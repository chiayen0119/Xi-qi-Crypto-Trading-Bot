$(document).ready(function(){

$("#btn").click( function refresh(){
    var currency = $("#currency").val();
    var resolution = $("#resolution").val();
    var startequity =$("#startequity").val();
    var date1 = $("#date1").val();
    var date2 = $("#date2").val();
    var strategy = $("#strategy").val();
    $("#load").show();
    $("#load1").show();
    $("#load2").show();
     $.ajax({
        type: 'GET', //傳送方式
        url: "/result", //傳送目的地
        data: {
            'currency':currency,
            'resolution':resolution,
            'startequity':startequity,
            'date1':date1,
            'date2':date2,
            'strategy':strategy
            },
        success: function(Data) {
            a=Data;
            $("#load").hide()
            $("#load1").hide()
            $("#load2").hide()
            if ($("#home").hasClass('active'))
            {
            $("#menu1").addClass('active');
            $("#result").html(Data.abc);
            $("#result2").html(Data.per);
            $("#result3").html(Data.trade);
            $("#result4").html(Data.score);
            $("#menu1").removeClass('active')};

            if ($("#menu2").hasClass('active'))
            {
            $("#menu1").addClass('active');
            $("#home").addClass('active');
            $("#result").html(Data.abc);
            $("#result2").html(Data.per);
            $("#result3").html(Data.trade);
            $("#result4").html(Data.score);
            $("#menu1").removeClass('active')
            $("#home").removeClass('active')};


            if ($("#menu1").hasClass('active'))
            {
            $("#home").addClass('active');
            $("#result").html(Data.abc);
            $("#result2").html(Data.per);
            $("#result3").html(Data.trade);
            $("#result4").html(Data.score);
            $("#home").removeClass('active')};
            },
            

            error: function(e) {
                console.log(e);
            },
            
        });
        
        $(window).resize(function(){
            if ($("#home").hasClass('active'))
            {
            $("#menu1").addClass('active');
            $("#result3").html(a.trade);
            $("#menu1").removeClass('active')};
        
            if ($("#menu2").hasClass('active'))
            {
            $("#menu1").addClass('active');
            $("#home").addClass('active');
            $("#result2").html(a.per);
            $("#result3").html(a.trade);
            $("#menu1").removeClass('active')
            $("#home").removeClass('active')};
        
        
            if ($("#menu1").hasClass('active'))
            {
            $("#home").addClass('active');
            $("#result2").html(a.per);
            $("#home").removeClass('active')};
            
        
        });    

        
    });
    

});


   
