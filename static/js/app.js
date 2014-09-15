window.fbAsyncInit = function() {
  FB.init({
    appId      : '767075363357147',
    xfbml      : true,
    version    : 'v2.0'
  });

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
        callback();
    }

    // set events
    function setEventHandlers(){
        // check if logged in facebook, reflect the state of the button
        checkLoginState();

        // logout button
        $('#fb-logout').click(logout);
        
        // login button
        $('#fb-login').click(function(){
            if(!checkLoginState()){
                login();
            }
        });

        // form submit
        $('#post-form').submit(function(){
            if(checkLoginState()){
                var msg = $('#post-form > textarea').val();
                postToFB(msg);
                return true;
            }
            else{
                return false;
            }
        });
    }

    // check if logged in facebook
    function checkLoginState(){
        FB.getLoginStatus(function(response){
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
        });
    }

    // post to facebook
    function postToFB(callback){
        var url = baseUrl + user.userID + "/feed/";
        var data = {
                    method: "post",
                    message: callback,
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
        user=callback.authResponse;
    }


    // login function
    function login(){
        FB.login(function(response){
            if(response.authResponse){
                getFBresponse(response);
                toggleLogin();
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




initialize(setEventHandlers);