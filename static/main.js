$(document).ready(function(){
    document.getElementById("query_box").addEventListener("keyup", function(){
        const temp = document.getElementById("query_box").value;
        console.log(temp)

        if(temp == ""){
            document.getElementById("response").innerHTML = "";
            console.log("Field empty");
        }
        else
        {
            $.ajax({
                url:"/sem_search",
                type : "GET",
                contentType : "application/json",
                data : {query_text : temp},
                success : function(response){
                    document.getElementById("response").innerHTML = response;
                    console.log("Got response");
                },
                error : function(error){
                    console.log("Error", error);
                }
            });
        }
    });

})