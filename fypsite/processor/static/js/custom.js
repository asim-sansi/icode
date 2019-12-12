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
                            getText : $('#Check1').prop("checked")
                        },// multiple data sent using ajax
                        dataType: "json",
                        success: function (response) {
                          alert(response['data']);
                        },
                        error: function(){
                          alert("Something went wrong while processing image.\nTry again in a while.");
                          return;
                        }
                    });
                }

            }