$(function(){

  if ($('pre').data().updateable) {
    setInterval(function(){
      $.get(window.location.pathname, function(res){
        $('pre').text(res)
      })
      console.log('ran')
    }, 5000)
  }

})