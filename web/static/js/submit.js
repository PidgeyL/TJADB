function autocomplete_wrapper(orig_id, eng_id, orig, eng) {
    $(orig_id).change(function() {
        var index = jQuery.inArray( $(orig_id).val() , orig);
        if( index !== -1 ){
            $(eng_id).val( eng[index] );
            generate_suggestion();
        }
    })

    $(eng_id).change(function() {
        var index = jQuery.inArray( $(eng_id).val() , eng);
        if( index !== -1 ){
            $(orig_id).val( orig[index] );
            generate_suggestion();
        }
    })
};

function generate_suggestion(){
    var artist_orig = $("#artist_orig").val();
    var artist_eng  = $("#artist_eng" ).val();
    var source_orig = $("#source_orig").val();
    var source_eng  = $("#source_eng" ).val();
    if (source_orig || source_eng){
        var sub_orig = "--" + artist_orig + "「" + source_orig + "」より";
        var sub_eng  = "--" + artist_orig + " from “" + source_orig + "”";
        $("#subtitle_suggest_orig").val(sub_orig);
        $("#subtitle_suggest_eng" ).val(sub_eng);
    }else{
        $("#subtitle_suggest_orig").val("--"+artist_orig);
        $("#subtitle_suggest_eng" ).val("--"+artist_eng);
    }
}

$(document).ready(function () {
    $("#sub_accept").click(function() {

        $("#subtitle_orig").val( $("#subtitle_suggest_orig").val() );
        $("#subtitle_eng" ).val( $("#subtitle_suggest_eng").val() );
    });

    $("#tja_parse").click(function() {
        var file = $("#tja_file")[0].files[0];
        if (typeof file == 'undefined'){
            return;
        }
        if (file.size > 51200) {
            alert('Max TJA size is 50k');
        }else{
            form = new FormData()
            form.append('file', file)
            $.ajax({
                url: 'parse_tja',
                type: 'POST',
                contentType: false,
                processData: false,
                data: form,
                success: function(response){
                    if(response != 0){
                        if (response['status'] == 'success'){
                            data = response['data']
                            $('#bpm'          ).val(data['bpm'])
                            $('#d_kantan'     ).val(data['easy'])
                            $('#genre'        ).val(data['genre'])
                            $('#d_muzukashii' ).val(data['hard'])
                            $('#d_futsuu'     ).val(data['normal'])
                            $('#d_oni'        ).val(data['oni'])
                            $('#subtitle_orig').val(data['sub'])
                            $('#subtitle_eng' ).val(data['sub'])
                            $('#title_orig'   ).val(data['title'])
                            $('#title_eng'    ).val(data['title'])
                            $('#d_ura'        ).val(data['ura'])
                        }else{
                            alert(response['message'])
                        }
                    }else{
                        alert('Could not parse TJA');
                    }
                },
            });
        }
    });
});
