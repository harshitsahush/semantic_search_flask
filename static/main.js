$(document).ready(function(){
    //function for throttling
    //https://dev.to/jeetvora331/throttling-in-javascript-easiest-explanation-1081
    function throttle(mainfn, delay)
    {
        let timerflag = null;
        return (...args) => {
            if(timerflag === null)
            {
                mainfn(...args);
                timerflag = setTimeout(() => {
                    timerflag = null;
                }, delay);
            }
        };
    }

    // calls API and updates data
    function fetchdata(){
        const temp = document.getElementById("query_box").value;
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

    const throttle_fetchdata = throttle(fetchdata, 500);

    document.getElementById("query_box").addEventListener("keyup", function(){
        const temp = document.getElementById("query_box").value;
        console.log(temp)

        if(temp == ""){
            document.getElementById("response").innerHTML = "";
            console.log("Field empty");
        }
        else
        {
            throttle_fetchdata()
        }
    });

})