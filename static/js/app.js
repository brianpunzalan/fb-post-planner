window.fbAsyncInit = function() {
    FB.init({
      appId      : '767075363357147',
      xfbml      : true,
      version    : 'v2.1',
      cookie     : true
    });
    initialize(setEventHandlers);
};
(function(d, s, id){
     var js, fjs = d.getElementsByTagName(s)[0];
     if (d.getElementById(id)) {return;}
     js = d.createElement(s); js.id = id;
     js.src = "//connect.facebook.net/en_US/sdk.js";
     fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

    var user;
    var baseUrl = "https://graph.facebook.com/v2.1/";

    function initialize(callback) {
        console.log("initialize");
        callback();
    }

    // set events
    function setEventHandlers(){
        // check if logged in facebook, reflect the state of the button
        checkLoginState();

        function submitForm(){
            $('#access_token').val(user.accessToken);
            $('#userID').val(user.userID);
            alert("submit");
            if(checkLoginState()){
                alert("yes");
                return true;
            }
            else{
                if(login()){
                    alert("logged in");
                    return true;
                }else{
                    return false;    
                }
            }
        }

        $("#post-form [name='date_to_post']").keypress(function(ev){
            ev.preventDefault();
        });

        $('#home').click(function(){
            $('#listpage').hide();
            $('#homepage').fadeIn("slow");
        });


        $('#lists').click(function(){
            $('#homepage').hide();
            $('#listpage').fadeIn("slow")
        });

        $('#btn-schedule-post').click(function(){
            alert("in");
            $('#post-form').submit(function(){
                alert("test");
            });
        });

        $('#btn-post-now').click(function(){
            $('#post-form').submit(submitForm);
        });

        // logout button
        $('#fb-logout').click(logout);
        
        // login button
        $('#fb-login').click(function(){
            console.log("login");
            if(!checkLoginState()){
                login();
            }
        });

        // form submit

        
        // $('#post-form').submit(function(){
        //     $('#access_token').val(user.accessToken);
        //     $('#userID').val(user.userID);
        //     //console.log($('#post-form message').val())
        //     // var msg = $('#post-form > textarea').val();
        //     // $('#post-form [name="access_token"]').val(user.accessToken);
        //     // $('#post-form [name="userID"]').val(user.userID);    
        //     alert("submit");
        //     if(checkLoginState()){
        //         alert("yes");
        //         //postToFB(msg);
        //         //$(this).attr('action','/fbpost?message='+msg+'&access_token='+user.access_token+'&userID='+user.userID)
        //         //console.log("submitting")
        //         //$('#post-form [name="access_token"]').val(user.access_token);
        //         //$('#post-form [name="userID"]').val(user.userID);
        //         return true;
        //     }
        //     else{
        //         if(login()){
        //             alert("logged in");
        //             //postToFB(msg);
        //             //$(this).attr('action','/fbpost?message='+msg+'&access_token='+user.access_token+'&userID='+user.userID)
        //             //console.log("ipost");
        //             //$('#post-form [name="access_token"]').val(user.access_token);
        //             //$('#post-form [name="userID"]').val(user.userID);
        //             return true;
        //         }else{
        //             return false;    
        //         }
        //     }
            
        // });
    }

    // user status
    function statusChangeCallback(response){
        console.log(response.status);
        if(response.status === 'connected'){
            setUserData(response);
            //alert("Connected!");
            toggleLogin();
            return true;
        }
        else if(response.status === 'not_authorized'){
            //alert("Not Authorized! Please Log into this application");
            return false;
        }
        else{
            //alert("Please Log into Facebook.");
            return false;
        }
    }

    // check if logged in facebook
    function checkLoginState(){
        FB.getLoginStatus(function(response){
            return statusChangeCallback(response);
        });
    }

    // post to facebook
    function postToFB(message){
        var url = baseUrl + user.userID + "/feed/";
        var data = {
                    method: "post",
                    message: message,
                    access_token: user.accessToken
                };
        $.get(url,data,function(response){
                    if(response.id){
                        alert('Post Successful');
                        var msg = $("#post-form textarea").val("");
                    }else{
                        alert('An error occured. Try to reload the page and try again.')
                    }
                }); 
    }


    // set value to variable 'user'
    function setUserData(callback){
        user = callback.authResponse;
    }

    // login function
    function login(){
        FB.login(function(response){
            if(response.authResponse){
                console.log(response.authResponse.userID);
                console.log(response.authResponse.access_token);
                console.log(response.authResponse.expiresIn);
                console.log(response.authResponse.signedRequest);
                setUserData(response);
                toggleLogin();
                return true;
            }
            else{
                return false;
            }
        }, {scope: 'publish_actions',return_scopes:true});
    }

    // logout function
    function logout(){
        FB.logout(function(){
            toggleLogin();
            user=null;
        });
    }


    // toggle login/logout buttons
    function toggleLogin(){
        $("#fb-login,#fb-logout").toggle();
    }

    $(function () {
        $('#datetimepicker').datetimepicker({ startDate: new Date() });
    });