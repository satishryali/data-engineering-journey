"use strict";
const { execFile } = require('child_process');

function playAlert() {
    return new Promise((resolve, reject) => {
        let command;
        let args;
        if (process.platform === 'win32') {
            command = 'powershell.exe';
            args = ['-NoProfile', '-NonInteractive', '-WindowStyle', 'Hidden', '-Command',
                '[System.Media.SystemSounds]::Exclamation.Play(); Start-Sleep -Milliseconds 1200'];
        } else if (process.platform === 'darwin') {
            command = '/usr/bin/afplay';
            args = ['/System/Library/Sounds/Tink.aiff'];
        } else {
            command = 'aplay';
            args = ['/usr/share/sounds/alsa/Front_Center.wav'];
        }
        execFile(command, args, { windowsHide: true, timeout: 5000 }, error => {
            if (error) reject(error);
            else resolve();
        });
    });
}
module.exports = { playAlert };
