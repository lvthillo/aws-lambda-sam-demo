function showInput() {
    docid = document.getElementById("document_id").value
    vid = document.getElementById("version_id").value;

    var result="";
    $.ajax({
        //url: "http://127.0.0.1:3000/document?documentId=" +docid + "&versionId=" + vid,
        url: "https://m5mah8v2r3.execute-api.eu-west-1.amazonaws.com/Prod/document?documentId=" +docid + "&versionId=" + vid,
        async: true,
        type: 'GET',
        success:function(data) {
            result = data; 
            document.getElementById('output').innerHTML = result['message']['location']
        }
   });
}