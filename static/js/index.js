function confirmation(id){
    
    str1 = "Are you sure you want to delete the record?<a href='delete/";
    str2 = id;
    str3 = "'>Yes</a>/<span onclick='cancel();'>No</span>";
    str4 = str1.concat(str2)
    str5 = str4.concat(str3)
    document.getElementById('confirmation').innerHTML=str5;
}

function cancel(){
    document.getElementById('confirmation').innerHTML = "";
}