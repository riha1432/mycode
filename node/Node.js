var http = require('http'); 
var fs = require('fs')
var app = require('express')();

// 2. http 모듈로 서버를 생성한다.
//    아래와 같이 작성하면 서버를 생성한 후, 사용자로 부터 http 요청이 들어오면 function 블럭내부의 코드를 실행해서 응답한다.
var server = http.createServer(function(request,response){ 
    var url = request.url;
    console.log(url);
    if(url == '/'){
        url = '/video.html';
        
        response.writeHead(200,{'Content-Type':'text/html'});
        response.end(fs.readFileSync(__dirname + url));
    }

    if(request.url == '/favicon.ico'){
        return response.writeHead(404);
    }
    
    // response.end(fs.readFileSync(__dirname + '/templates/video.html'));
});

app.get('/video_feed', function(req, res){
    console.log('video_feed');
    fs.readFile('./runs/detect/predict/image0.jpg', function(err,data){
        console.log('picture loading...');
        response.writeHead(200);
        response.write(data);
        response.end(); 
    });
});

// 3. listen 함수로 8080 포트를 가진 서버를 실행한다. 서버가 실행된 것을 콘솔창에서 확인하기 위해 'Server is running...' 로그를 출력한다
server.listen(8080, function(){ 
    console.log('Server is running...');
});

