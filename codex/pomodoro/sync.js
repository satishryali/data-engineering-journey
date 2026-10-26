"use strict";

// Drive transports these files. It is eventually consistent, not a distributed lock.
const fs = require('node:fs');
const path = require('node:path');
const { randomUUID } = require('node:crypto');
const { todayKey, weekStart } = require('./stats');
const uuid = value => typeof value === 'string' && /^[a-f0-9-]{36}$/.test(value);
const day = value => typeof value === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(value)
    && !Number.isNaN(Date.parse(value)) && new Date(value).toISOString().slice(0, 10) === value;
const integer = value => Number.isSafeInteger(value) && value >= 0;
function valid(record) {
    if (!record || record.version !== 1) return false;
    if (record.type === 'baseline') return uuid(record.id) && record.counts
        && !Array.isArray(record.counts) && typeof record.counts === 'object'
        && Object.entries(record.counts).every(([key, value]) => day(key) && integer(value));
    if (!uuid(record.owner) || !integer(record.claim) || record.claim < 1) return false;
    if (record.type === 'completion') return uuid(record.focusId) && day(record.day);
    return record.type === 'state' && uuid(record.focusId) && integer(record.revision)
        && ['work', 'shortBreak', 'longBreak'].includes(record.phase)
        && ['idle', 'paused', 'running'].includes(record.state)
        && integer(record.remaining) && record.remaining <= 86400 && integer(record.cycles)
        && typeof record.savedAt === 'string' && !Number.isNaN(Date.parse(record.savedAt));
}
function compare(a, b) {
    return a.claim - b.claim || a.owner.localeCompare(b.owner) || (a.revision || 0) - (b.revision || 0);
}
class SharedTimer {
    constructor(folder) {
        if (!path.isAbsolute(folder)) throw Error('Choose an absolute path to a synced timer folder.');
        for (let parent = path.resolve(folder); ; parent = path.dirname(parent)) {
            if (fs.existsSync(path.join(parent, '.git'))) throw Error('Choose a timer folder outside the Git repository.');
            if (path.dirname(parent) === parent) break;
        }
        this.folder = folder;
        this.owner = randomUUID(); // A new VS Code window always starts as an observer.
        this.latest = undefined;
        this.records = [];
    }
    read() {
        const records = [];
        for (const name of fs.readdirSync(this.folder)) {
            // Ignore temporary uploads and unrelated files; accept Drive conflict copies.
            if (!/^(baseline|state-|complete-).*\.json$/.test(name)) continue;
            const filename = path.join(this.folder, name);
            if (fs.statSync(filename).size > 1024 * 1024) throw Error(`Unexpected timer file size: ${name}`);
            const record = JSON.parse(fs.readFileSync(filename, 'utf8'));
            if (!valid(record)) throw Error(`Invalid timer data: ${name}. Waiting for a valid sync copy.`);
            records.push(record);
        }
        const baselines = records.filter(record => record.type === 'baseline');
        if (!baselines.length) throw Error('Shared history has not arrived. Wait for Drive sync, or initialise it on the original computer.');
        if (new Set(baselines.map(record => JSON.stringify(record))).size !== 1)
            throw Error('Conflicting shared baselines. Preserve the files and reconcile them before continuing.');
        this.baseline = baselines[0];
        this.records = records;
        this.latest = records.filter(record => record.type === 'state').sort(compare).at(-1);
        return this.latest;
    }
    write(name, record) {
        if (!valid(record)) throw Error('Refusing to write invalid timer data.');
        const temporary = path.join(this.folder, `.${randomUUID()}.tmp`);
        try {
            fs.writeFileSync(temporary, JSON.stringify(record), { flag: 'wx' });
            fs.renameSync(temporary, path.join(this.folder, name));
        } finally {
            if (fs.existsSync(temporary)) fs.unlinkSync(temporary);
        }
    }
    initialise(counts) {
        if (fs.readdirSync(this.folder).length) throw Error('Create history in an empty folder, once, on the original computer.');
        const baseline = { version: 1, type: 'baseline', id: randomUUID(), counts };
        this.write('baseline.json', baseline);
        this.read();
    }
    owns() { return this.latest?.owner === this.owner; }
    takeover(fallback) {
        this.read();
        const previous = this.latest;
        const next = previous ? { ...previous } : { ...fallback, focusId: randomUUID() };
        // Keep the saved remaining time. Never infer work from time spent powered off.
        next.state = next.state === 'idle' ? 'idle' : 'paused';
        next.claim = (previous?.claim || 0) + 1;
        next.owner = this.owner;
        next.revision = 0;
        return this.save(next);
    }
    save(snapshot) {
        const record = { ...snapshot, version: 1, type: 'state', owner: this.owner,
            revision: snapshot.revision + 1, savedAt: new Date().toISOString() };
        this.write(`state-${this.owner}.json`, record);
        this.latest = record;
        return record;
    }
    publish(snapshot) {
        this.read();
        if (!this.owns()) throw Error('Another computer controls this timer. Use Continue session here to take over.');
        return this.save({ ...this.latest, ...snapshot });
    }
    completed(focusId) {
        return this.records.some(record => record.type === 'completion' && record.focusId === focusId);
    }
    complete(date = todayKey()) {
        this.read();
        if (!this.owns()) throw Error('Another computer controls this timer.');
        const { focusId, claim } = this.latest;
        if (this.completed(focusId)) return;
        const record = { version: 1, type: 'completion', focusId, claim, owner: this.owner, day: date };
        this.write(`complete-${focusId}-${this.owner}.json`, record);
        this.records.push(record);
    }
    counts() {
        const counts = { ...this.baseline.counts };
        const completions = new Map();
        for (const record of this.records) {
            if (record.type !== 'completion') continue;
            const old = completions.get(record.focusId);
            if (!old || compare(record, old) > 0) completions.set(record.focusId, record);
        }
        for (const record of completions.values()) counts[record.day] = (counts[record.day] || 0) + 1;
        return counts;
    }
    summary(date = todayKey()) {
        const counts = this.counts();
        const start = weekStart(date);
        const end = new Date(`${start}T00:00:00Z`);
        end.setUTCDate(end.getUTCDate() + 7);
        const stop = end.toISOString().slice(0, 10);
        return { today: counts[date] || 0, week: Object.entries(counts)
            .filter(([key]) => key >= start && key < stop).reduce((sum, [, value]) => sum + value, 0),
        overall: Object.values(counts).reduce((sum, value) => sum + value, 0), weekStart: start };
    }
}
module.exports = { SharedTimer, valid };
