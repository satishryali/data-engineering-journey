"use strict";

// Keep the extension's existing date-keyed history; resets select a new period.
const PREFIX = 'pomodoro.stats.';
function todayKey(now = new Date()) {
    return new Intl.DateTimeFormat('en-CA', {
        timeZone: 'Asia/Kolkata', year: 'numeric', month: '2-digit', day: '2-digit'
    }).format(now);
}
function weekStart(dateKey) {
    const date = new Date(`${dateKey}T00:00:00Z`);
    date.setUTCDate(date.getUTCDate() - (date.getUTCDay() + 6) % 7);
    return date.toISOString().slice(0, 10);
}
class StatsManager {
    constructor(storage, options = {}) {
        this.storage = storage;
        this.externalCounts = options.externalCounts;
        this.startDate = options.startDate || '';
        this.pending = Promise.resolve();
        if (this.startDate) {
            const seedKey = `pomodoro.journey.baseline.${this.startDate}`;
            this.baseline = storage.get(seedKey);
            if (!this.baseline) {
                this.baseline = { raw: this.rawCount(this.startDate), count: options.initialCount || 0 };
                this.pending = storage.update(seedKey, this.baseline);
            } else if (Number.isSafeInteger(options.initialCount) && options.initialCount > this.baseline.count) {
                // A reported correction raises the baseline once, without dropping later completions.
                this.baseline = { ...this.baseline, count: options.initialCount };
                this.pending = storage.update(seedKey, this.baseline);
            }
        }
    }
    reportedCounts() {
        if (this.externalCounts) return this.externalCounts;
        try {
            return require('vscode').workspace.getConfiguration('pomodoro')
                .get('externalCompletedSessions', {}) || {};
        } catch { return {}; }
    }
    rawCount(dateKey) {
        const value = this.storage.get(PREFIX + dateKey, 0);
        return Number.isSafeInteger(value) && value > 0 ? value : 0;
    }
    getCount(dateKey) {
        if (this.startDate && dateKey < this.startDate) return 0;
        const raw = this.rawCount(dateKey);
        const reported = this.reportedCounts()[dateKey];
        const extra = Number.isSafeInteger(reported) && reported > 0 ? reported : 0;
        return (dateKey === this.startDate
            ? Math.max(0, raw - this.baseline.raw + this.baseline.count) : raw) + extra;
    }
    incrementCount(dateKey) {
        const write = this.pending.then(async () => {
            const count = this.rawCount(dateKey) + 1;
            await this.storage.update(PREFIX + dateKey, count);
            return this.getCount(dateKey);
        });
        this.pending = write.catch(() => {});
        return write;
    }
    getSummary(dateKey = todayKey()) {
        const start = weekStart(dateKey);
        const end = new Date(`${start}T00:00:00Z`);
        end.setUTCDate(end.getUTCDate() + 7);
        const exclusiveEnd = end.toISOString().slice(0, 10);
        let week = 0;
        let overall = 0;
        const keys = new Set(this.storage.keys());
        for (const day of Object.keys(this.reportedCounts())) keys.add(PREFIX + day);
        for (const key of keys) {
            if (!/^pomodoro\.stats\.\d{4}-\d{2}-\d{2}$/.test(key)) continue;
            const day = key.slice(PREFIX.length);
            if (this.startDate && day < this.startDate) continue;
            const count = this.getCount(day);
            overall += count;
            if (day >= start && day < exclusiveEnd) week += count;
        }
        // The reported starting count exists even if no timer history key exists yet.
        if (this.startDate && !keys.has(PREFIX + this.startDate)) {
            const count = this.getCount(this.startDate);
            overall += count;
            if (this.startDate >= start && this.startDate < exclusiveEnd) week += count;
        }
        return { today: this.getCount(dateKey), week, overall, weekStart: start };
    }
}
function dailyTarget(dateKey, weekday = 14, weekend = 20) {
    const day = new Date(`${dateKey}T00:00:00Z`).getUTCDay();
    return day === 0 || day === 6 ? weekend : weekday;
}
function formatSummary(counts, dateKey = todayKey(), options = {}) {
    const weekday = options.weekdayTarget || 14;
    const weekend = options.weekendTarget || 20;
    const target = dailyTarget(dateKey, weekday, weekend);
    const weekly = options.weeklyTarget || weekday * 5 + weekend * 2;
    const day = new Intl.DateTimeFormat('en', { weekday: 'long', timeZone: 'UTC' })
        .format(new Date(`${dateKey}T00:00:00Z`));
    return `Today (${day}, IST): ${counts.today}/${target} | Remaining today: ${Math.max(0, target - counts.today)} | This week (Mon-Sun): ${counts.week}/${weekly} | Overall: ${counts.overall} | Remaining this week: ${Math.max(0, weekly - counts.week)}`;
}
module.exports = { StatsManager, todayKey, weekStart, dailyTarget, formatSummary };
