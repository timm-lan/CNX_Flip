/**
 * Created by openstax on 6/16/17.
 */
$('.message a').click(function(){
    $('form').animate({height: "toggle", opacity: "toggle"}, "slow");
});