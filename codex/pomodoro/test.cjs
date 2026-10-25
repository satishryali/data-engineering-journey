const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const { StatsManager, todayKey, weekStart, dailyTarget, formatSummary } = require('./stats');
function memory(initial = {}) {
    return { data: { ...initial }, keys() { return Object.keys(this.data); },
        get(key, fallback) { return this.data[key] ?? fallback; },
        async update(key, value) { this.data[key] = value; } };
}
async function main() {
    assert.equal(todayKey(new Date('2026-10-25T18:29:59Z')), '2026-10-25');
    assert.equal(todayKey(new Date('2026-10-25T18:30:00Z')), '2026-10-26');
    assert.equal(weekStart('2026-10-25'), '2026-10-19');
    assert.equal(weekStart('2026-10-26'), '2026-10-26');
    assert.equal(weekStart('2027-01-01'), '2026-12-28');
    const storage = memory({ 'pomodoro.stats.2026-10-18': 3, 'pomodoro.stats.2026-10-19': 4,
        'pomodoro.stats.2026-10-25': 2, 'pomodoro.stats.2026-10-26': 1,
        'pomodoro.stats.garbage': 100, 'unrelated': 100 });
    const stats = new StatsManager(storage);
    assert.deepEqual(stats.getSummary('2026-10-25'), { today: 2, week: 6, overall: 10, weekStart: '2026-10-19' });
    assert.deepEqual(stats.getSummary('2026-10-26'), { today: 1, week: 1, overall: 10, weekStart: '2026-10-26' });
    assert.deepEqual(stats.getSummary('2026-11-02'), { today: 0, week: 0, overall: 10, weekStart: '2026-11-02' });
    await Promise.all([stats.incrementCount('2026-10-26'), stats.incrementCount('2026-10-26')]);
    assert.equal(stats.getCount('2026-10-26'), 3);
    assert.equal(dailyTarget('2026-10-25'), 20);
    assert.equal(dailyTarget('2026-10-24'), 20);
    for (const day of ['26', '27', '28', '29', '30']) assert.equal(dailyTarget(`2026-10-${day}`), 14);
    const seededStorage = memory({ 'pomodoro.stats.2026-10-24': 9, 'pomodoro.stats.2026-10-25': 7 });
    let seeded = new StatsManager(seededStorage, { startDate: '2026-10-25', initialCount: 3 });
    await seeded.pending;
    assert.deepEqual(seeded.getSummary('2026-10-25'), { today: 3, week: 3, overall: 3, weekStart: '2026-10-19' });
    assert.match(formatSummary(seeded.getSummary('2026-10-25'), '2026-10-25'), /Sunday, IST\): 3\/20.*Remaining today: 17/);
    assert.equal(await seeded.incrementCount('2026-10-25'), 4);
    seeded = new StatsManager(seededStorage, { startDate: '2026-10-25', initialCount: 3 });
    assert.equal(seeded.getCount('2026-10-25'), 4, 'reload never seeds again');
    assert.equal(seededStorage.get('pomodoro.stats.2026-10-24'), 9, 'old history retained');
    assert.deepEqual(seeded.getSummary('2026-10-26'), { today: 0, week: 0, overall: 4, weekStart: '2026-10-26' });
    const blank = new StatsManager(memory(), { startDate: '2026-10-25', initialCount: 3 });
    assert.equal(blank.getSummary('2026-10-25').overall, 3);
    await blank.incrementCount('2026-10-25');
    assert.equal(blank.getSummary('2026-10-25').overall, 4, 'seed counted once when first history key is created');
    const reported = memory({ 'pomodoro.stats.2026-10-25': 4,
        'pomodoro.journey.baseline.2026-10-25': { raw: 4, count: 3 } });
    let corrected = new StatsManager(reported, { startDate: '2026-10-25', initialCount: 4 });
    await corrected.pending;
    assert.equal(corrected.getSummary('2026-10-25').today, 4, 'recover completion made before customization reload');
    assert.equal(await corrected.incrementCount('2026-10-25'), 5);
    corrected = new StatsManager(reported, { startDate: '2026-10-25', initialCount: 4 });
    assert.equal(corrected.getCount('2026-10-25'), 5, 'correction is not added again on reload');
    assert.match(formatSummary({ today: 22, week: 112, overall: 112 }, '2026-10-25'), /Remaining today: 0.*Remaining this week: 0/);
    const fixture = process.argv[2];
    assert.ok(fixture, 'Pass the customized extension fixture path');
    const timerModule = { exports: {} };
    vm.runInNewContext(fs.readFileSync(path.join(fixture, 'out/timer.js'), 'utf8'), {
        exports: timerModule.exports, setInterval: () => 1, clearInterval: () => {}
    });
    let timer;
    class ObservedTimer extends timerModule.exports.Timer {
        constructor(config) { super(config); timer = this; }
    }
    const commands = {};
    const notifications = [];
    let sounds = 0;
    let menu;
    const statusBar = { show() {} };
    const settings = { enableAudio: true, enableNotifications: true, enableCelebration: false,
        weeklyTarget: 110, sessionDuration: 25, shortBreakDuration: 5, longBreakDuration: 15,
        longBreakInterval: 4, autoStart: false };
    const vscode = {
        StatusBarAlignment: { Left: 1 },
        window: { createStatusBarItem: () => statusBar,
            showInformationMessage: async text => { notifications.push(text); },
            showWarningMessage: text => { throw Error(text); },
            showQuickPick: async items => { menu = items; } },
        commands: { registerCommand: (name, fn) => { commands[name] = fn; return {}; },
            executeCommand: async name => commands[name]?.() },
        workspace: { getConfiguration: () => ({ get: (key, fallback) => settings[key] ?? fallback }),
            onDidChangeConfiguration: () => ({}) }
    };
    const exports = {};
    vm.runInNewContext(fs.readFileSync(path.join(fixture, 'out/extension.js'), 'utf8'), {
        exports, setTimeout, require: name => {
            if (name === 'vscode') return vscode;
            if (name === './timer') return { Timer: ObservedTimer };
            if (name === './audio') return { playAlert: async () => { sounds++; } };
            if (name === './stats') return require(path.join(fixture, 'out/stats.js'));
            return require(name);
        }
    });
    const history = memory();
    exports.activate({ globalState: history, subscriptions: [] });
    const settle = () => new Promise(resolve => setImmediate(resolve));
    commands['pomodoro.start']();
    timer.forceTimeRemaining(1); timer.tick(); await settle();
    assert.equal(timer.getPhase(), 'shortBreak');
    assert.equal(timer.getTimeRemaining(), 300);
    assert.equal(sounds, 1);
    commands['pomodoro.start']();
    timer.forceTimeRemaining(1); timer.tick(); await settle();
    assert.equal(timer.getPhase(), 'work');
    assert.equal(sounds, 2);
    commands['pomodoro.stats']();
    assert.match(notifications.at(-1), /Today \(.*IST\): 1\/(14|20).*1\/110.*Overall: 1.*109/);
    assert.match(statusBar.text, /\| 1\/(14|20)/);
    await commands['pomodoro.showMenu']();
    assert.ok(menu.some(item => item.command === 'pomodoro.testSound'));
    menu.find(item => item.label.includes('Skip Phase')).action(); await settle();
    assert.equal(timer.getWorkCyclesCompleted(), 1);
    assert.equal(sounds, 2, 'skips do not ring or count');
    commands['pomodoro.stats']();
    assert.match(notifications.at(-1), /Overall: 1/);
    await commands['pomodoro.testSound'](); assert.equal(sounds, 3);
    settings.enableAudio = false;
    commands['pomodoro.start'](); timer.forceTimeRemaining(1); timer.tick(); await settle();
    assert.equal(sounds, 3, 'muted completion does not ring');
    exports.deactivate();
    console.log('PASS: daily targets, one-time reported baseline, retained history, reload, IST boundaries, concurrent saves, real timer/extension integration, sound, skip and mute.');
}
main().catch(error => { console.error(error); process.exitCode = 1; });
