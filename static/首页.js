window.onload=function() {
    var ul = document.getElementById("slider1");

    function show() {
        var left = ul.offsetLeft - 360; //获取left值
        ul.style.left = left + "px"; //设置left值
        console.log(ul.style.left)
        //走完一半再返回
        // 		console.log(ul.offsetLeft)
        // 		console.log(ul.offsetWidth)
        //走完一半再返回
        if (-1 * ul.offsetLeft >= ul.offsetWidth / 2) {
            ul.style.left = 0;
        }
    }

    var t = setInterval(show, 1200);


     var ull = document.getElementById("slider2");

    function show2() {
        var left = ull.offsetLeft - 360; //获取left值
        ull.style.left = left + "px"; //设置left值

        //走完一半再返回
        if (-1 * ull.offsetLeft >= ull.offsetWidth / 2) {
            ull.style.left = 0;
        }
    }
        var t2 = setInterval(show2, 1200);

    //-------------------轮播图结束----------------------------------------
    var radMin = 5,
        radMax = 125,
        filledCircle = 60, //percentage of filled circles
        concentricCircle = 30, //percentage of concentric circles
        radThreshold = 25; //IFF special, over this radius concentric, otherwise filled

//min and max speed to move
    var speedMin = 0.3,
        speedMax = 2.5;

//max reachable opacity for every circle and blur effect
    var maxOpacity = 0.6;

//default palette choice
    var colors = ['52,168,83', '117,95,147', '199,108,23', '194,62,55', '0,172,212', '120,120,120'],
        bgColors = ['52,168,83', '117,95,147', '199,108,23', '194,62,55', '0,172,212', '120,120,120'],
        circleBorder = 10,
        backgroundLine = bgColors[0];
    var backgroundMlt = 0.85;

    var canvas = document.getElementById("canvas");

//min distance for links
    var linkDist = Math.min(canvas.offsetWidth, canvas.offsetHeight) / 2.4,
        lineBorder = 2.5;

//most importantly: number of overall circles and arrays containing them
    var maxCircles = 12,
        points = [],
        pointsBack = [];

//populating the screen
    for (var i = 0; i < maxCircles * 2; i++) points.push(new Circle());
    for (var i = 0; i < maxCircles; i++) pointsBack.push(new Circle(true));

//experimental vars
    var circleExp = 1,
        circleExpMax = 1.003,
        circleExpMin = 0.997,
        circleExpSp = 0.00004,
        circlePulse = false;

//circle class
    function Circle(background) {
        //if background, it has different rules
        this.background = (background || false);
        this.x = randRange(-canvas.width / 2, canvas.width / 2);
        this.y = randRange(-canvas.height / 2, canvas.height / 2);
        this.radius = background ? hyperRange(radMin, radMax) * backgroundMlt : hyperRange(radMin, radMax);
        this.filled = this.radius < radThreshold ? (randint(0, 100) > filledCircle ? false : 'full') : (randint(0, 100) > concentricCircle ? false : 'concentric');
        this.color = background ? bgColors[randint(0, bgColors.length - 1)] : colors[randint(0, colors.length - 1)];
        this.borderColor = background ? bgColors[randint(0, bgColors.length - 1)] : colors[randint(0, colors.length - 1)];
        this.opacity = 0.05;
        this.speed = (background ? randRange(speedMin, speedMax) / backgroundMlt : randRange(speedMin, speedMax)); // * (radMin / this.radius);
        this.speedAngle = Math.random() * 2 * Math.PI;
        this.speedx = Math.cos(this.speedAngle) * this.speed;
        this.speedy = Math.sin(this.speedAngle) * this.speed;
        var spacex = Math.abs((this.x - (this.speedx < 0 ? -1 : 1) * (canvas.width / 2 + this.radius)) / this.speedx),
            spacey = Math.abs((this.y - (this.speedy < 0 ? -1 : 1) * (canvas.height / 2 + this.radius)) / this.speedy);
        this.ttl = Math.min(spacex, spacey);
    };

    Circle.prototype.init = function () {
        Circle.call(this, this.background);
    }

//support functions
//generate random int a<=x<=b
    function randint(a, b) {
        return Math.floor(Math.random() * (b - a + 1) + a);
    }

    //generate random float
    function randRange(a, b) {
        return Math.random() * (b - a) + a;
    }

    //generate random float more likely to be close to a
    function hyperRange(a, b) {
        return Math.random() * Math.random() * Math.random() * (b - a) + a;
    }

//rendering function
    function drawCircle(ctx, circle) {
        //circle.radius *= circleExp;
        var radius = circle.background ? circle.radius *= circleExp : circle.radius /= circleExp;
        ctx.beginPath();
        ctx.arc(circle.x, circle.y, radius * circleExp, 0, 2 * Math.PI, false);
        ctx.lineWidth = Math.max(1, circleBorder * (radMin - circle.radius) / (radMin - radMax));
        ctx.strokeStyle = ['rgba(', circle.borderColor, ',', circle.opacity, ')'].join('');
        if (circle.filled == 'full') {
            ctx.fillStyle = ['rgba(', circle.borderColor, ',', circle.background ? circle.opacity * 0.8 : circle.opacity, ')'].join('');
            ctx.fill();
            ctx.lineWidth = 0;
            ctx.strokeStyle = ['rgba(', circle.borderColor, ',', 0, ')'].join('');
        }
        ctx.stroke();
        if (circle.filled == 'concentric') {
            ctx.beginPath();
            ctx.arc(circle.x, circle.y, radius / 2, 0, 2 * Math.PI, false);
            ctx.lineWidth = Math.max(1, circleBorder * (radMin - circle.radius) / (radMin - radMax));
            ctx.strokeStyle = ['rgba(', circle.color, ',', circle.opacity, ')'].join('');
            ctx.stroke();
        }
        circle.x += circle.speedx;
        circle.y += circle.speedy;
        if (circle.opacity < (circle.background ? maxOpacity : 1)) circle.opacity += 0.01;
        circle.ttl--;
    }

//initializing function
    function init() {
        window.requestAnimationFrame(draw);
    }

//rendering function
    function draw() {

        if (circlePulse) {
            if (circleExp < circleExpMin || circleExp > circleExpMax) circleExpSp *= -1;
            circleExp += circleExpSp;
        }
        var ctxfr = document.getElementById('canvas').getContext('2d');
        var ctxbg = document.getElementById('canvasbg').getContext('2d');

        ctxfr.globalCompositeOperation = 'destination-over';
        ctxfr.clearRect(0, 0, canvas.width, canvas.height); // clear canvas
        ctxbg.globalCompositeOperation = 'destination-over';
        ctxbg.clearRect(0, 0, canvas.width, canvas.height); // clear canvas

        ctxfr.save();
        ctxfr.translate(canvas.width / 2, canvas.height / 2);
        ctxbg.save();
        ctxbg.translate(canvas.width / 2, canvas.height / 2);

        //function to render each single circle, its connections and to manage its out of boundaries replacement
        function renderPoints(ctx, arr) {
            for (var i = 0; i < arr.length; i++) {
                var circle = arr[i];
                //checking if out of boundaries
                if (circle.ttl < 0) {
                }
                var xEscape = canvas.width / 2 + circle.radius,
                    yEscape = canvas.height / 2 + circle.radius;
                if (circle.ttl < -20) arr[i].init(arr[i].background);
                //if (Math.abs(circle.y) > yEscape || Math.abs(circle.x) > xEscape) arr[i].init(arr[i].background);
                drawCircle(ctx, circle);
            }
            for (var i = 0; i < arr.length - 1; i++) {
                for (var j = i + 1; j < arr.length; j++) {
                    var deltax = arr[i].x - arr[j].x;
                    var deltay = arr[i].y - arr[j].y;
                    var dist = Math.pow(Math.pow(deltax, 2) + Math.pow(deltay, 2), 0.5);
                    //if the circles are overlapping, no laser connecting them
                    if (dist <= arr[i].radius + arr[j].radius) continue;
                    //otherwise we connect them only if the dist is < linkDist
                    if (dist < linkDist) {
                        var xi = (arr[i].x < arr[j].x ? 1 : -1) * Math.abs(arr[i].radius * deltax / dist);
                        var yi = (arr[i].y < arr[j].y ? 1 : -1) * Math.abs(arr[i].radius * deltay / dist);
                        var xj = (arr[i].x < arr[j].x ? -1 : 1) * Math.abs(arr[j].radius * deltax / dist);
                        var yj = (arr[i].y < arr[j].y ? -1 : 1) * Math.abs(arr[j].radius * deltay / dist);
                        ctx.beginPath();
                        ctx.moveTo(arr[i].x + xi, arr[i].y + yi);
                        ctx.lineTo(arr[j].x + xj, arr[j].y + yj);
                        var samecolor = arr[i].color == arr[j].color;
                        ctx.strokeStyle = ["rgba(", arr[i].borderColor, ",", Math.min(arr[i].opacity, arr[j].opacity) * ((linkDist - dist) / linkDist), ")"].join("");
                        ctx.lineWidth = (arr[i].background ? lineBorder * backgroundMlt : lineBorder) * ((linkDist - dist) / linkDist); //*((linkDist-dist)/linkDist);
                        ctx.stroke();
                    }
                }
            }
        }

        var startTime = Date.now();
        renderPoints(ctxfr, points);
        renderPoints(ctxbg, pointsBack);
        deltaT = Date.now() - startTime;

        ctxfr.restore();
        ctxbg.restore();

        window.requestAnimationFrame(draw);
    }

    init();

    var radMin = 5,
        radMax = 125,
        filledCircle = 60, //percentage of filled circles
        concentricCircle = 30, //percentage of concentric circles
        radThreshold = 25; //IFF special, over this radius concentric, otherwise filled

//min and max speed to move
    var speedMin = 0.3,
        speedMax = 2.5;

//max reachable opacity for every circle and blur effect
    var maxOpacity = 0.6;

//default palette choice
    var colors = ['52,168,83', '117,95,147', '199,108,23', '194,62,55', '0,172,212', '120,120,120'],
        bgColors = ['52,168,83', '117,95,147', '199,108,23', '194,62,55', '0,172,212', '120,120,120'],
        circleBorder = 10,
        backgroundLine = bgColors[0];
    var backgroundMlt = 0.85;

    var canvas = document.getElementById("canvas");

//min distance for links
    var linkDist = Math.min(canvas.offsetWidth, canvas.offsetHeight) / 2.4,
        lineBorder = 2.5;

//most importantly: number of overall circles and arrays containing them
    var maxCircles = 12,
        points = [],
        pointsBack = [];

//populating the screen
    for (var i = 0; i < maxCircles * 2; i++) points.push(new Circle());
    for (var i = 0; i < maxCircles; i++) pointsBack.push(new Circle(true));

//experimental vars
    var circleExp = 1,
        circleExpMax = 1.003,
        circleExpMin = 0.997,
        circleExpSp = 0.00004,
        circlePulse = false;

//circle class
    function Circle(background) {
        //if background, it has different rules
        this.background = (background || false);
        this.x = randRange(-canvas.width / 2, canvas.width / 2);
        this.y = randRange(-canvas.height / 2, canvas.height / 2);
        this.radius = background ? hyperRange(radMin, radMax) * backgroundMlt : hyperRange(radMin, radMax);
        this.filled = this.radius < radThreshold ? (randint(0, 100) > filledCircle ? false : 'full') : (randint(0, 100) > concentricCircle ? false : 'concentric');
        this.color = background ? bgColors[randint(0, bgColors.length - 1)] : colors[randint(0, colors.length - 1)];
        this.borderColor = background ? bgColors[randint(0, bgColors.length - 1)] : colors[randint(0, colors.length - 1)];
        this.opacity = 0.05;
        this.speed = (background ? randRange(speedMin, speedMax) / backgroundMlt : randRange(speedMin, speedMax)); // * (radMin / this.radius);
        this.speedAngle = Math.random() * 2 * Math.PI;
        this.speedx = Math.cos(this.speedAngle) * this.speed;
        this.speedy = Math.sin(this.speedAngle) * this.speed;
        var spacex = Math.abs((this.x - (this.speedx < 0 ? -1 : 1) * (canvas.width / 2 + this.radius)) / this.speedx),
            spacey = Math.abs((this.y - (this.speedy < 0 ? -1 : 1) * (canvas.height / 2 + this.radius)) / this.speedy);
        this.ttl = Math.min(spacex, spacey);
    };

    Circle.prototype.init = function () {
        Circle.call(this, this.background);
    }

//support functions
//generate random int a<=x<=b
    function randint(a, b) {
        return Math.floor(Math.random() * (b - a + 1) + a);
    }

    //generate random float
    function randRange(a, b) {
        return Math.random() * (b - a) + a;
    }

    //generate random float more likely to be close to a
    function hyperRange(a, b) {
        return Math.random() * Math.random() * Math.random() * (b - a) + a;
    }

//rendering function
    function drawCircle(ctx, circle) {
        //circle.radius *= circleExp;
        var radius = circle.background ? circle.radius *= circleExp : circle.radius /= circleExp;
        ctx.beginPath();
        ctx.arc(circle.x, circle.y, radius * circleExp, 0, 2 * Math.PI, false);
        ctx.lineWidth = Math.max(1, circleBorder * (radMin - circle.radius) / (radMin - radMax));
        ctx.strokeStyle = ['rgba(', circle.borderColor, ',', circle.opacity, ')'].join('');
        if (circle.filled == 'full') {
            ctx.fillStyle = ['rgba(', circle.borderColor, ',', circle.background ? circle.opacity * 0.8 : circle.opacity, ')'].join('');
            ctx.fill();
            ctx.lineWidth = 0;
            ctx.strokeStyle = ['rgba(', circle.borderColor, ',', 0, ')'].join('');
        }
        ctx.stroke();
        if (circle.filled == 'concentric') {
            ctx.beginPath();
            ctx.arc(circle.x, circle.y, radius / 2, 0, 2 * Math.PI, false);
            ctx.lineWidth = Math.max(1, circleBorder * (radMin - circle.radius) / (radMin - radMax));
            ctx.strokeStyle = ['rgba(', circle.color, ',', circle.opacity, ')'].join('');
            ctx.stroke();
        }
        circle.x += circle.speedx;
        circle.y += circle.speedy;
        if (circle.opacity < (circle.background ? maxOpacity : 1)) circle.opacity += 0.01;
        circle.ttl--;
    }

//initializing function
    function init() {
        window.requestAnimationFrame(draw);
    }

//rendering function
    function draw() {

        if (circlePulse) {
            if (circleExp < circleExpMin || circleExp > circleExpMax) circleExpSp *= -1;
            circleExp += circleExpSp;
        }
        var ctxfr = document.getElementById('canvas').getContext('2d');
        // var ctxbg = document.getElementById('canvasbg').getContext('2d');

        ctxfr.globalCompositeOperation = 'destination-over';
        ctxfr.clearRect(0, 0, canvas.width, canvas.height); // clear canvas
        // ctxbg.globalCompositeOperation = 'destination-over';
        // ctxbg.clearRect(0, 0, canvas.width, canvas.height); // clear canvas

        ctxfr.save();
        ctxfr.translate(canvas.width / 2, canvas.height / 2);
        // ctxbg.save();
        // ctxbg.translate(canvas.width / 2, canvas.height / 2);

        //function to render each single circle, its connections and to manage its out of boundaries replacement
        function renderPoints(ctx, arr) {
            for (var i = 0; i < arr.length; i++) {
                var circle = arr[i];
                //checking if out of boundaries
                if (circle.ttl < 0) {
                }
                var xEscape = canvas.width / 2 + circle.radius,
                    yEscape = canvas.height / 2 + circle.radius;
                if (circle.ttl < -20) arr[i].init(arr[i].background);
                //if (Math.abs(circle.y) > yEscape || Math.abs(circle.x) > xEscape) arr[i].init(arr[i].background);
                drawCircle(ctx, circle);
            }
            for (var i = 0; i < arr.length - 1; i++) {
                for (var j = i + 1; j < arr.length; j++) {
                    var deltax = arr[i].x - arr[j].x;
                    var deltay = arr[i].y - arr[j].y;
                    var dist = Math.pow(Math.pow(deltax, 2) + Math.pow(deltay, 2), 0.5);
                    //if the circles are overlapping, no laser connecting them
                    if (dist <= arr[i].radius + arr[j].radius) continue;
                    //otherwise we connect them only if the dist is < linkDist
                    if (dist < linkDist) {
                        var xi = (arr[i].x < arr[j].x ? 1 : -1) * Math.abs(arr[i].radius * deltax / dist);
                        var yi = (arr[i].y < arr[j].y ? 1 : -1) * Math.abs(arr[i].radius * deltay / dist);
                        var xj = (arr[i].x < arr[j].x ? -1 : 1) * Math.abs(arr[j].radius * deltax / dist);
                        var yj = (arr[i].y < arr[j].y ? -1 : 1) * Math.abs(arr[j].radius * deltay / dist);
                        ctx.beginPath();
                        ctx.moveTo(arr[i].x + xi, arr[i].y + yi);
                        ctx.lineTo(arr[j].x + xj, arr[j].y + yj);
                        var samecolor = arr[i].color == arr[j].color;
                        ctx.strokeStyle = ["rgba(", arr[i].borderColor, ",", Math.min(arr[i].opacity, arr[j].opacity) * ((linkDist - dist) / linkDist), ")"].join("");
                        ctx.lineWidth = (arr[i].background ? lineBorder * backgroundMlt : lineBorder) * ((linkDist - dist) / linkDist); //*((linkDist-dist)/linkDist);
                        ctx.stroke();
                    }
                }
            }
        }

        var startTime = Date.now();
        renderPoints(ctxfr, points);
        // renderPoints(ctxbg, pointsBack);
        deltaT = Date.now() - startTime;

        ctxfr.restore();
        // ctxbg.restore();

        window.requestAnimationFrame(draw);
    }

    init();
}




  // var ul = document.getElementsByClassName("ul")[0];
	// 	function show() {
	// 		var left = ul.offsetLeft - 1; //获取left值
	// 		ul.style.left = left + "px"; //设置left值
  //           console.log(ul.offsetLeft)
	// 		//console.log(ul.style.left)
	// //走完一半再返回
  //
  //   		//console.log(ul.offsetWidth)
	// 			//走完一半再返回
	// 		if (-1 * ul.offsetLeft >= ul.offsetWidth / 2) {
	// 			ul.style.left = 0;
	// 		}
	// 	}
	// 	var t = setInterval(show, 10);






    /**************************** ***********轮播图**********************************************************/
// var box = document.getElementById('box1');
// 		var slider = document.getElementById('slider');
// 		var left = document.getElementById('left');
// 		var right = document.getElementById('right');
// 		// var oNavlist = document.getElementById('nav').children;
// 		var index = 1; //打开页面生效的图片的下标为1
// 		// var timer;
// 		var isMoving = false;
// 		// box.onmouseover = function () {
// 		// 	animate(left, {
// 		// 		opacity: 0.6
// 		// 	})
// 		// 	animate(right, {
// 		// 		opacity: 0.6
// 		// 	})
// 		// 	clearInterval(timer); //图片停止滚动
// 		// }
// 		// box.onmouseout = function () {
// 		// 	animate(left, {
// 		// 		opacity: 0
// 		// 	})
// 		// 	animate(right, {
// 		// 		opacity: 0
// 		// 	})
// 		// 	timer = setInterval(next, 3000); //图片开始接着滚动
// 		// }
// 		right.onclick = next;
// 		left.onclick = prev;
//
// 		function next() {
// 			if (isMoving) {
// 				return;
// 			}
// 			isMoving = true;
// 			index++;
// 			// navmove();
// 			animate(slider, {
// 				left: -500 * index
// 			}, function () {
// 				if (index == 4) {
// 					slider.style.left = '-1000px';
// 					index = 1;
// 				}
// 				isMoving = false;
// 			});
// 		}
//
// 		function prev() {
// 			if (isMoving) {
// 				return;
// 			}
// 			isMoving = true;
// 			index--;
// 			// navmove();
// 			animate(slider, {
// 				left: -500 * index
// 			}, function () {
// 				if (index == 0) {
// 					slider.style.left = '-1500px';
// 					index = 3;
// 				}
// 				isMoving = false;
// 			});
// 		}
// 		//页面打开时自动滚动切换
// 		timer = setInterval(next, 1000);
//
//
// 		  function getStyle(obj, attr) { //返回值带有单位px
//   	if (obj.currentStyle) {
//   		return obj.currentStyle[attr];
//   	} else {
//   		return getComputedStyle(obj, null)[attr];
//   	}
//   }
//
//   // function animate(obj, json, callback) {
//   // 	clearInterval(obj.timer);
//   // 	obj.timer = setInterval(function () {
//   // 		var flag = true;
//   // 		for (var attr in json) {
//   // 			(function (attr) {
//   // 				if (attr == "opacity") {
//   // 					var now = parseInt(getStyle(obj, attr) * 100);
//   // 					var dest = json[attr] * 100;
//   // 				} else {
//   // 					var now = parseInt(getStyle(obj, attr));
//   // 					var dest = json[attr];
//   // 				}
//   // 				// var speed = (dest - now) / 6;
//   //               var speed = dest - now;
//   // 				speed = speed > 0 ? Math.ceil(speed) : Math.floor(speed);
//   // 				if (now != dest) {
//   // 					flag = false;
//   // 					if (attr == "opacity") {
//   // 						obj.style[attr] = (now + speed) / 100;
//   // 					} else {
//   // 						obj.style[attr] = now + speed + "px";
//   // 					}
//   // 				}
//   // 			})(attr);
//   // 		}
//   // 		if (flag) {
//   // 			clearInterval(obj.timer);
//   // 			callback && callback(); //如果回调函数存在，就调用回调函数
//   // 		}
//   // 	}, 30);
//   }
//
// /*****************************结束********************************/
//
// }




