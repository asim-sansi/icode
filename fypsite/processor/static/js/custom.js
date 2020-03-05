            var img = new Image();

            function readURL(input) {
                if (input.files && input.files[0]) {
                    var reader = new FileReader();

                    reader.onload = function (e) {
                        $('#view_image').attr('src', e.target.result);
                        img.src = e.target.result;
                        $('#initiate').removeClass("disabled");
                        $('#initiate').css('cursor', 'pointer');
                    };
                    reader.readAsDataURL(input.files[0]);
                }
            }
            function beginTranslation(){
                if(!$('#initiate').hasClass("disabled")){
                    // imgElem must be on the same server otherwise a cross-origin error will be thrown "SECURITY_ERR: DOM Exception 18"
                    var canvas = document.createElement("canvas");
                    canvas.width = img.width;
                    canvas.height = img.height;
                    var ctx = canvas.getContext("2d");
                    ctx.drawImage(img, 0, 0);
                    var dataURL = canvas.toDataURL("image/png");
                    var imgData = dataURL.replace(/^data:image\/(png|jpg);base64,/, "");
                    $.ajax({
                        type:"POST",
                        cache:false,
                        url:"./startprocess/",
                        data:{
                            imageData : imgData,
                            textType : $("input[name=text-type]:checked").val(),
                            imageType : $("input[name=image-type]:checked").val()
                        },// multiple data sent using ajax
                        dataType: "json",
                        success: function (response) {
                          alert(response['data']);
                          trackTranslation();
                          return;
                        },
                        error: function(){
                          alert("Something went wrong while processing image.\nTry again in a while.");
                          return;
                        }
                    });
                }

            }

            function trackTranslation(){
                var complete = 0;
                $('#progress-bar').parent().css("background", "#222");
                $('#result-nav').css("display", "none");
                const intervalLength = 100;
                const interval = setInterval(() => {
                    $.ajax({
                        url:"./trackprocess/",
                        dataType: "json",
                        success: function (response) {
                            console.log(response['progress'])
                            if(response['progress'] == 100){
                                complete = 100;
                                document.getElementById("progress-bar").style.width = complete.toString() + "%";
                                document.getElementById("progress-bar").innerText = complete.toString() + "%";
                                $('#result-nav').css("display", "inline-flex");
                                clearInterval(interval);
                            }
                            else if (response['progress'] >= 0){
                                complete = response['progress']
                                document.getElementById("progress-bar").style.width = complete.toString() + "%";
                                document.getElementById("progress-bar").innerText = complete.toString() + "%";
                            }
                        },
                        error: function(){

                            return;
                        }
                    });
                }, intervalLength);

            }

            function viewpage(){
                $.ajax({
                    url:"./viewpage/",
                    dataType: "json",
                    success: function (response) {
                        console.log["progress"]
                        return;
                    },
                    error: function(){
                        return;
                    }
                });
            }
            
            function downloadfile(){
                // $.ajax({
                //     url:"./download/",
                //     dataType: "json",
                //     success: function (response) {
                //         return;
                //     },
                //     error: function(){
                //         return;
                //     }
                // });
                $("body").append('<iframe src="./download/" style="display: none;" ></iframe>');

            }