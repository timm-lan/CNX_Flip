function do_some_ajax(){
    jQuery.ajax({
        url     : 'ajax_view',
        type    : 'POST',
        dataType: 'json',
        success : function(data){                                     //***
            alert("Success. Got the message:\n "+ data.message)       //***
        }                                                             //***
    });
    //alert("TODO: implement ajax call");
}
