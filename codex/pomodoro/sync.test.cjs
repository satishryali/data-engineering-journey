const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const vm = require('node:vm');
const { SharedTimer } = require('./sync');
const { attach } = require('./sync-vscode');
const { StatsManager } = require('./stats');
const folders = [];
function temporary() {
    const folder = fs.mkdtempSync(path.join(os.tmpdir(), 'journey-pomodoro-test-'));
    folders.push(folder);
    return folder;
}
const fresh = { phase: 'work', state: 'idle', remaining: 1500, cycles: 0 };
async function main() {
    assert.throws(() => new SharedTimer(__dirname), /outside the Git/);
    const folder = temporary();
    const desktop = new SharedTimer(folder);
    desktop.initialise({ '2026-10-25': 4, '2026-10-26': 3 });
    const laptop = new SharedTimer(folder);
    laptop.read();
    assert.equal(laptop.summary('2026-10-26').today, 3);
    assert.equal(laptop.summary('2026-10-26').overall, 7);
    assert.throws(() => laptop.initialise({}), /empty folder/);
    desktop.takeover(fresh);
    desktop.publish({ ...fresh, state: 'running', remaining: 731 });
    assert.equal(laptop.takeover(fresh).remaining, 731);
    assert.equal(laptop.latest.state, 'paused', 'power-off gap is excluded');
    assert.throws(() => desktop.publish(fresh), /Another computer/);
    const focusId = laptop.latest.focusId;
    laptop.complete('2026-10-26');
    laptop.complete('2026-10-26');
    assert.equal(laptop.summary('2026-10-26').today, 4, 'same focus counts once');
    const completion = laptop.records.find(record => record.type === 'completion');
    fs.writeFileSync(path.join(folder, 'complete-conflict-copy.json'), JSON.stringify(completion));
    laptop.read();
    assert.equal(laptop.summary('2026-10-26').today, 4, 'Drive conflict copies cannot duplicate a completion');
    const restarted = new SharedTimer(folder);
    restarted.read();
    assert.equal(restarted.owns(), false, 'reopening VS Code never automatically takes ownership');
    assert.equal(restarted.latest.focusId, focusId);
    assert.equal(restarted.completed(focusId), true, 'completion survives a crash before phase snapshot');
    fs.writeFileSync(path.join(folder, 'state-incomplete.json'), '{');
    assert.throws(() => restarted.read(), SyntaxError);
    fs.unlinkSync(path.join(folder, 'state-incomplete.json'));
    fs.writeFileSync(path.join(folder, 'baseline-conflict.json'), JSON.stringify({ ...desktop.baseline, counts: {} }));
    assert.throws(() => restarted.read(), /Conflicting/);
    fs.unlinkSync(path.join(folder, 'baseline-conflict.json'));

    // Two delayed Drive replicas can claim concurrently. On arrival they converge;
    // the completion identity, rather than the computer identity, prevents duplicates.
    const replica = temporary();
    for (const name of fs.readdirSync(folder)) fs.copyFileSync(path.join(folder, name), path.join(replica, name));
    const offline = new SharedTimer(replica);
    const online = new SharedTimer(folder);
    offline.takeover(fresh);
    online.takeover(fresh);
    for (const name of fs.readdirSync(replica)) fs.copyFileSync(path.join(replica, name), path.join(folder, name));
    online.read();
    offline.folder = folder;
    offline.read();
    assert.equal(Number(online.owns()) + Number(offline.owns()), 1);
    assert.equal(online.summary('2026-10-26').today, 4);

    const fixture = process.argv[2];
    assert.ok(fixture, 'Pass an installed extension fixture for real timer integration');
    const timerModule = { exports: {} };
    vm.runInNewContext(fs.readFileSync(path.join(fixture, 'out/timer.js'), 'utf8'), {
        exports: timerModule.exports, setInterval: () => 1, clearInterval() {}
    });
    const bridgeFolder = temporary();
    new SharedTimer(bridgeFolder).initialise({ '2026-10-25': 4 });
    function device() {
        const commands = {};
        const warnings = [];
        const subscriptions = [];
        const settings = { syncFolder: bridgeFolder };
        const storage = { keys: () => [], get: (_, fallback) => fallback, update: async () => {} };
        const timer = new timerModule.exports.Timer({ work: 25, shortBreak: 5, longBreak: 15, longBreakInterval: 4 });
        const stats = new StatsManager(storage);
        const vscode = { commands: { registerCommand(name, fn) { commands[name] = fn; return { dispose() {} }; } },
            workspace: { getConfiguration: () => ({ get: (key, fallback) => settings[key] ?? fallback }) },
            window: { showWarningMessage: text => warnings.push(text), showInformationMessage: async () => 'Continue Here' } };
        const context = { subscriptions, globalState: storage };
        attach({ context, vscode, timer, stats, refresh() {} });
        return { timer, stats, commands, warnings, dispose() { for (const sub of subscriptions) sub.dispose(); } };
    }
    const d1 = device();
    const d2 = device();
    try {
        d1.timer.start();
        assert.equal(d1.timer.getState(), 'idle', 'a passive device cannot accidentally start');
        await d1.commands['pomodoro.continueHere']();
        assert.equal(d1.timer.getState(), 'running');
        d1.timer.forceTimeRemaining(700);
        d1.timer.pause();
        await d2.commands['pomodoro.continueHere']();
        assert.equal(d2.timer.getTimeRemaining(), 700);
        assert.equal(d2.timer.getState(), 'running');
        d1.timer.tick();
        assert.equal(d1.timer.getState(), 'paused', 'former controller stops when a takeover arrives');
        assert.equal(d1.timer.getTimeRemaining(), 700);
        const date = require('./stats').todayKey();
        const before = d2.stats.getSummary(date).today;
        d2.timer.forceTimeRemaining(1);
        d2.timer.tick();
        assert.equal(d2.timer.getPhase(), 'shortBreak');
        assert.equal(d2.stats.getSummary(date).today, before + 1);
        d2.timer.skip();
        assert.equal(d2.stats.getSummary(date).today, before + 1, 'skipping break does not count focus');
        const nextFocus = new SharedTimer(bridgeFolder);
        nextFocus.read();
        const firstId = nextFocus.latest.focusId;
        d2.timer.reset();
        nextFocus.read();
        assert.notEqual(nextFocus.latest.focusId, firstId, 'reset persists a fresh identity');
        d2.timer.start();
        d2.timer.forceTimeRemaining(1);
        d2.timer.tick();
        assert.equal(d2.stats.getSummary(date).today, before + 2, 'new focus session counts separately');
        assert.equal(d2.stats.getSummary('2026-10-25').today, 4, 'baseline appears once on every device');
        d2.timer.start();
        fs.writeFileSync(path.join(bridgeFolder, 'state-broken.json'), '{');
        d2.timer.tick();
        assert.notEqual(d2.timer.getState(), 'running', 'invalid sync data stops countdown');
        fs.unlinkSync(path.join(bridgeFolder, 'state-broken.json'));
    } finally { d1.dispose(); d2.dispose(); }
    // Crash recovery at the completion/state boundary must open on a break.
    const recovery = new SharedTimer(bridgeFolder);
    recovery.takeover(fresh);
    recovery.publish({ ...fresh, remaining: 0 });
    recovery.complete();
    const d3 = device();
    try {
        assert.equal(d3.timer.getPhase(), 'shortBreak');
        assert.equal(d3.timer.getState(), 'idle');
    } finally { d3.dispose(); }
    console.log('PASS: shared baseline, takeover, frozen downtime, stale controller, reload, duplicate/conflict copies, delayed replicas, corrupt data, real timer completion/skip/reset and crash recovery.');
}
main().catch(error => { console.error(error); process.exitCode = 1; }).finally(() => {
    for (const folder of folders) {
        const resolved = path.resolve(folder);
        const prefix = path.join(os.tmpdir(), 'journey-pomodoro-test-');
        if (resolved.startsWith(prefix)) fs.rmSync(resolved, { recursive: true, force: true });
    }
});
