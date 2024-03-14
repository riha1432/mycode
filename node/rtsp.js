// const app = require('express')(),
//   server = require('http').Server(app),
//   io = require('socket.io')(server),
//   rtsp = require('rtsp-ffmpeg');

// server.listen(6148); //열고싶은 포트번호 입력
// var uri = 'rtsp://210.99.70.120:1935/live/cctv001.stream', 
//   stream = new rtsp.FFMpeg({input: uri});

// io.on('connection', function(socket) {
//   var pipeStream = function(data) {
//     socket.emit('data', data.toString('base64'));
//   };
//   stream.on('data', pipeStream);
//   socket.on('disconnect', function() {
//     stream.removeListener('data', pipeStream);
//   });
// });

// app.get('/', function (req, res) {
//   res.sendFile(__dirname + '/rtsphtml.html');
// });

const express = require('express');
const WebSocket = require('ws');
const app = express();
const server = app.listen(3000, () => {
console.log('Server started on port 3000');
});
const wss = new WebSocket.Server({ server });
wss.on('connection', (ws) => {
console.log('WebSocket connected');
// WebSocket에서 메시지 받을 때 처리하는 부분
ws.on('message', (message) => {
console.log(`Received message: ${message}`);
});
});
const { spawn } = require('child_process');
const ffmpeg = spawn('ffmpeg', [
'-i', 'rtsp://210.99.70.120:1935/live/cctv001.stream',
'-f', 'mpegts',
'-codec:v', 'mpeg1video',
'-s', '640x480',
'-b:v', '800k',
'-bf', '0',
'-muxdelay', '0.001',
'-']);
ffmpeg.stdout.on('data', (data) => {
// ffmpeg 출력 데이터를 WebSocket으로 전송
wss.clients.forEach((client) => {
if (client.readyState === WebSocket.OPEN) {
client.send(data);
}
});
});
ffmpeg.stderr.on('data', (data) => {
console.error(`ffmpeg stderr: ${data}`);
});
ffmpeg.on('close', (code) => {
console.log(`ffmpeg process exited with code ${code}`);
});