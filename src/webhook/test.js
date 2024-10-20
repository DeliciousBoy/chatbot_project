// test.js
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

// ร่วมเส้นทาง
const fullPath = path.join(__dirname,'functions','utils','gemini.py');
// const doubleBackslashPath = fullPath.replace('\' , '\\');
// ข้อมูล input ที่ต้องการส่งไปยัง Python

const userInput = "มีกระเบื้องอะไรบ้าง";
// เรียกใช้งาน Python script พร้อมส่ง userInput

// exec(`python ${fullPath} "${userInput}"`, (error, stdout, stderr) => {
//     // if (error) {
//     //     console.error(`Error executing Python script: ${error.message}`);
//     //     return;
//     // }
//     // if (stderr) {
//     //     console.error(`Python error: ${stderr}`);
//     //     return;
//     // }

//     // แปลง output จาก Python script (ในรูปแบบ JSON) ให้เป็น JavaScript object
//     try {
//          var output = JSON.parse(stdout);
//         // resolve(output.result); 
//         console.log(output.result);
//     } catch (parseError) {
//         console.error(`Error parsing JSON: ${parseError.message}`);
//     }
// });

const CAT = process.env.CHANNEL_ACCESS_TOKEN;
const NT = process.env.NOTIFY_TOKEN;
console.log(CAT)