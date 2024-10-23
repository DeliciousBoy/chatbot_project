    if (error) {
        console.error(`Error executing Python script: ${error.message}`);
        return;
    }
    if (stderr) {
        console.error(`Python error: ${stderr}`);
        return;
    }