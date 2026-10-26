"use strict";

const { randomUUID } = require('node:crypto');
const { SharedTimer } = require('./sync');
const { todayKey } = require('./stats');

function attach({ context, vscode, timer, stats, refresh }) {
    const getConfig = () => vscode.workspace.getConfiguration('pomodoro');
    const folder = getConfig().get('syncFolder', '');
    const localSummary = stats.getSummary.bind(stats);
    const localIncrement = stats.incrementCount.bind(stats);
    let shared;
    let failure = '';
    let lastSave = 0;
    let stopped = false;
    const snapshot = () => ({ phase: timer.getPhase(), state: timer.getState(),
        remaining: timer.getTimeRemaining(), cycles: timer.getWorkCyclesCompleted() });
    function warn(error) {
        timer.stopInterval();
        if (timer.state === 'running') timer.state = 'paused';
        if (failure !== error.message) vscode.window.showWarningMessage(`Pomodoro sync: ${error.message}`);
        failure = error.message;
        refresh();
    }
    function restore(saved) {
        if (!saved) return;
        timer.stopInterval();
        timer.phase = saved.phase;
        timer.state = saved.state === 'idle' ? 'idle' : 'paused';
        timer.timeRemaining = Math.max(1, saved.remaining);
        timer.workCyclesCompleted = saved.cycles;
        // A crash after writing a completion but before saving the following phase
        // must not repeat that focus session or discard its completion.
        if (saved.phase === 'work' && shared.completed(saved.focusId)) {
            timer.workCyclesCompleted++;
            timer.phase = timer.workCyclesCompleted % timer.config.longBreakInterval === 0 ? 'longBreak' : 'shortBreak';
            timer.timeRemaining = timer.getDurationLimit(timer.phase) * 60;
            timer.state = 'idle';
        }
        refresh();
    }
    function poll() {
        if (!shared || stopped) return;
        try {
            const previous = shared.latest;
            const latest = shared.read();
            if (!shared.owns() && (!previous || latest?.owner !== previous.owner || latest?.revision !== previous.revision)) restore(latest);
            failure = '';
            refresh();
        } catch (error) { warn(error); }
    }
    function publish(extra = {}) {
        shared.publish({ ...snapshot(), ...extra });
        lastSave = Date.now();
    }
    function requireOwner() {
        if (!shared) throw Error('Sync is unavailable. Check the folder and reload VS Code.');
        shared.read();
        if (!shared.owns()) {
            restore(shared.latest);
            throw Error('Use Pomodoro: Continue Session Here before controlling the shared timer.');
        }
        failure = '';
    }

    context.subscriptions.push(vscode.commands.registerCommand('pomodoro.configureSync', async () => {
        if (timer.getState() === 'running') {
            vscode.window.showWarningMessage('Pause or finish the current Pomodoro before configuring sync.');
            return;
        }
        const folders = await vscode.window.showOpenDialog({ canSelectFiles: false, canSelectFolders: true,
            canSelectMany: false, openLabel: 'Use this Google Drive timer folder' });
        if (!folders?.length) return;
        const choice = await vscode.window.showQuickPick([
            { label: 'Create shared history from this computer', description: 'Original computer only. Import displayed counts once.', create: true },
            { label: 'Join existing shared history', description: 'Laptop or any later setup. Does not import local counts.', create: false }
        ], { placeHolder: 'Use the same synced folder on both computers' });
        if (!choice) return;
        try {
            const target = new SharedTimer(folders[0].fsPath);
            if (choice.create) {
                const counts = {};
                const keys = new Set(context.globalState.keys().filter(key => /^pomodoro\.stats\.\d{4}-\d{2}-\d{2}$/.test(key))
                    .map(key => key.slice('pomodoro.stats.'.length)));
                const config = getConfig();
                const start = config.get('trackingStartDate', '');
                if (start) keys.add(start);
                for (const key of Object.keys(config.get('externalCompletedSessions', {}))) keys.add(key);
                if (shared) {
                    shared.read();
                    Object.assign(counts, shared.counts());
                } else {
                    for (const key of keys) counts[key] = localSummary(key).today;
                }
                target.initialise(counts);
            } else target.read();
            // An absolute Drive path is a machine setting. Never put it in Git.
            await getConfig().update('syncFolder', folders[0].fsPath, vscode.ConfigurationTarget.Global);
            vscode.window.showInformationMessage('Pomodoro sync folder saved. Reload VS Code, then use Pomodoro: Continue Session Here.');
        } catch (error) { vscode.window.showWarningMessage(`Pomodoro sync setup: ${error.message}`); }
    }));
    context.subscriptions.push(vscode.commands.registerCommand('pomodoro.continueHere', async () => {
        if (!folder) {
            vscode.window.showInformationMessage('Run Pomodoro: Configure Sync Folder first.');
            return;
        }
        if (!shared) { warn(Error('Sync folder is unavailable. Check Drive and reload VS Code.')); return; }
        if (shared.owns() && timer.getState() === 'running') return;
        const answer = await vscode.window.showInformationMessage(
            'Check that Google Drive has finished syncing. Continue from the last saved remaining time here? Keep the other computer stopped.', 'Continue Here');
        if (answer !== 'Continue Here' || stopped) return;
        try {
            restore(shared.takeover(snapshot()));
            publish();
            timer.start();
        } catch (error) { warn(error); }
    }));
    if (!folder) return;
    try {
        shared = new SharedTimer(folder);
        shared.read();
    } catch (error) { warn(error); }

    // Folder configured but unreadable means controls fail closed, not a new local timer.
    stats.getSummary = date => shared?.baseline ? shared.summary(date) : localSummary(date);
    stats.incrementCount = async date => {
        if (!shared) throw Error('Shared session history is unavailable.');
        // Completion is persisted before the native timer changes phase.
        return shared.summary(date).today;
    };
    const oldTick = timer.tick.bind(timer);
    timer.tick = () => {
        try {
            requireOwner();
            oldTick();
            if (Date.now() - lastSave >= 5000) publish();
        } catch (error) { warn(error); }
    };
    for (const method of ['start', 'pause', 'reset', 'skip', 'updateConfig']) {
        const original = timer[method].bind(timer);
        timer[method] = (...args) => {
            try {
                requireOwner();
                if (method === 'start' && shared.latest.phase === 'work' && shared.completed(shared.latest.focusId)) restore(shared.latest);
                const result = original(...args);
                // Reset starts a fresh focus identity without removing historical counts.
                publish(method === 'reset' && timer.getPhase() === 'work' ? { focusId: randomUUID() } : {});
                return result;
            } catch (error) { warn(error); }
        };
    }
    const transition = timer.transitionPhase.bind(timer);
    timer.transitionPhase = (completed = true) => {
        requireOwner();
        const previous = timer.getPhase();
        if (completed && previous === 'work') shared.complete(todayKey());
        transition(completed);
        // The work identity survives computer takeovers but never a new work phase.
        publish(timer.getPhase() === 'work' ? { focusId: randomUUID() } : {});
    };
    restore(shared?.latest);
    const interval = setInterval(poll, 2000);
    context.subscriptions.push({ dispose() {
        stopped = true;
        clearInterval(interval);
        // The most recent periodic snapshot also survives abrupt shutdowns.
        if (shared?.owns()) {
            try { publish(); } catch { /* Retain the last successfully saved snapshot. */ }
        }
        timer.stopInterval();
        stats.incrementCount = localIncrement;
    } });
}
module.exports = { attach };
