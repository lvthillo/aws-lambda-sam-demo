function showInput() {
    docid = document.getElementById("document_id").value
    vid = document.getElementById("version_id").value;

    var result="";
    $.ajax({
        url: "http://127.0.0.1:3000/document?documentId=" +docid + "&versionId=" + vid,
        //url: "https://xxx.execute-api.ap-northeast-1.amazonaws.com/v1/document?documentId=" +docid + "&versionId=" + vid,
        async: true,
        type: 'GET',
        success:function(data) {
            result = data; 
            document.getElementById('output').innerHTML = result['message']['location']
        },
        error:function (xhr, ajaxOptions, thrownError){
            if(xhr.status==404) {
                document.getElementById('output').innerHTML = 'Item not found'
            }
            else {
                document.getElementById('output').innerHTML = 'Unexpected error'
            }
        }
   });
}