$(document).ready(function(){

$("#btn").click( function (){
    var Email = $("#Email").val();
    var API_key = $("#API_key").val();
    var API_secret =$("#API_secret").val();
    $("#board").append('trading start'+'</br>')
            var interval=setInterval(function(){
            $.ajax({
                type: 'GET', //傳送方式
                url: "/postreal", //傳送目的地
                data: {},
                success: function(Data) {
                        $("#board").append(Data+'</br>')
                    },
                    

                    error: function(e) {
                        console.log(e);
                    },
                
            });
        }, 1000);
        
    $("#btn2").click(function (){
                clearInterval(interval)
    });    
  


    $.ajax({
        type: 'GET', //傳送方式
        url: "/realresult", //傳送目的地
        data: {
            'Email':Email,
            'API_key':API_key,
            'API_secret':API_secret,
            },
        success: function(Data) {
            setTimeout(function(){$("#board").append(Data+'</br>')},100);


            },
            

            error: function(e) {
                console.log(e);
            },
            
        });

});


$("#btn2").click( function (){
    $.ajax({
        type: 'GET', //傳送方式
        url: "/realstop", //傳送目的地
        data: {},
        success: function(Data) {
            


        },
        

        error: function(e) {
            console.log(e);
        },
    });


});
});


   
