		$(document).ready(function(){
			//comment this out when not working on the backend
			//$("#constructionbox").modal({
            //    opacity: 80,
            //    closeClass: "exitbox",
            //	overlayCss: {backgroundColor:"#000"}
			//});
			$("#pDontcare").bind("click", function(){
				var randNum1 = Math.floor(Math.random(Date.UTC())*6400001);
				var randNum2 = Math.floor(Math.random(Date.UTC()*randNum1)*6400001) * Math.floor(Math.random()*64000001);
				var sRandNum1 = randNum1.toString();
				var sRandNum2 = randNum2.toString();
				var counter = 0;
				var fRandNum1 = new String;
				var fRandNum2 = new String;
				while (counter < sRandNum1.length){
					fRandNum1 = fRandNum1 + sRandNum1.charAt(counter);
					counter += Math.floor(Math.random()*8);
				}
				counter = 0;
				while (counter < sRandNum2.length ){
					fRandNum2 = fRandNum2 + sRandNum1.charAt(counter);
					counter += Math.floor(Math.random(Date.UTC()*counter)*8);
				}
				var sha1r1 = hex_sha1(fRandNum1);
				var sha1r2 = hex_md5(fRandNum2);
				$("#pkey1").val(sha1r1);
				$("#pkey2").val(sha1r2);
			});
			$("#deleteastory").bind("click",function(){
				$("#deletebox").modal({
					opacity: 80,
	                closeClass: "exitbox",
	            	overlayCss: {backgroundColor:"#000"}
				});
			});
			$("#tell").bind("click",function(){
				if (100 - $("#story").val().length <= 0){
					$.post("/addStory/",{storytext:$("#story").val()},function(data){
						if (data == "success"){
							window.location.reload();
						}
                        else if (data == "spam"){
                        	$.modal.close();
                            $("#spambox").modal({
                                opacity: 80,
                                closeClass: "exitbox",
                                overlayCss: {backgroundColor:"#000"}
                           });
                        }
                       else if (data == "repeat"){
                        	$.modal.close();
                            $("#repeatbox").modal({
                                opacity: 80,
                                closeClass: "exitbox",
                                overlayCss: {backgroundColor:"#000"}
                           });
                       }
                        else {
                        	$.modal.close();
                            $("#failbox").modal({
                                opacity: 80,
                                closeClass: "exitbox",
                                overlayCss: {backgroundColor:"#000"}
                            });
                        }
					});	
				}
			});
			$(".showhidelink").bind("click",function(){
				if ($("#storyContain").hasClass("open")){
					$("#storyContain").slideUp();
					$("#storyContain").removeClass("open");
					$(".showhidelink").html("<img src='/media/img/plus32.png' alt='Tell'/>");
				}
				else {
					$("#storyContain").slideDown();
					$("#storyContain").addClass("open");
					$(".showhidelink").html("<img src='/media/img/minus32.png' alt='Read'/>");
				}
			});
/*			$("#tell").bind('click',function(){
				if (100 - $("#story").val().length <= 0){
					$("#passkeybox").modal({
	                    opacity: 80,
	                    closeClass: "exitbox",
	                    overlayCss: {backgroundColor:"#000"}
					});
				}
                else {
                    $("#notlongenough").modal({
                        opacity: 80,
                        closeClass: "exitbox",
                        overlayCss: {backgroundColor:"#000"}
                    });
                }
			}); */
            $("#story").bind("keyup",function(){
                if (100 - $(this).val().length > 0){
                	if ($(".charsleft").hasClass("hidden")){
                		$(".charsleft").removeClass("hidden");
                		$(".charsleft").fadeIn();
                	}
                    $("#numchars").html(100-$(this).val().length);
                }
                else {
                	if (!$(".charsleft").hasClass("hidden")){
                		$(".charsleft").fadeOut();
                		$(".charsleft").addClass("hidden");
                	}
                }
            });
		$("#whytell").bind("click",function(){
			$("#whybox").modal({
				opacity: 80,
				closeClass: "exitbox",
				overlayCss: {backgroundColor:"#000"}
			});
		});
		$("#howtell").bind("click",function(){
			$("#howbox").modal({
				opacity: 80,
				closeClass: "exitbox",
				overlayCss: {backgroundColor:"#000"}
			});
		});

});