function download(ID) {
    if ($("#orig").prop("checked")){
      var type = "orig";
    }else{
      var type = "eng";
    }
    window.location.href = "/download/"+ type + '/' + ID;
}

$(document).ready(function () {
    var table = $('#dtSongTable').DataTable({
        "order": [[ 11, "desc" ]],
        "columnDefs": [
            { width: 27, targets: 4 },
            { width: 27, targets: 5 },
            { width: 27, targets: 6 },
            { width: 27, targets: 7 },
            { width: 27, targets: 8 },
            { visible: false, targets: 3 },
            { visible: false, targets: 9 },
            { visible: false, targets: 10 },
            { visible: false, targets: 11 }
        ],
        "autoWidth": false,
        "fixedColumns": true,
        "lengthMenu": [[25, 50, 100, 200, -1], [25, 50, 100, 200, "All"]],
        "pageLength" : 100,
    });
    $('.dataTables_length').addClass('bs-select');

    $('a.toggle-vis').on( 'click', function (e) {
        e.preventDefault();
        var column = table.column( $(this).attr('data-column') );
        column.visible( ! column.visible() );
    } );

    $('a.toggle-dif').on( 'click', function (e) {
        e.preventDefault();
        var first = $(this).attr('data-column');
        for (let i = first; i < parseInt(first)+5; i++) {
            var column = table.column( i );
            column.visible( ! column.visible() );
        }
    } );

});
