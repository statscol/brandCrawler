function Ntweets(val) {
    document.getElementById('ntweets').innerHTML=val; 
}

Ntweets("1500");

$(document).ready(function(){
	$('.btn').click(function(){
   		$('.loader').show();
	});
	$('.hidebtn').click(function(){
   		$('.myimgdivshowhide').hide();
	});
 });