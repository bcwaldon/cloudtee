$(function(){

  if ($('pre').data().updateable) {
    setInterval(function(){
      $.get('/zomgwtfbbq', function(res){
        $('pre').text(res)
      })
      console.log('ran')
    }, 5000)
  }

})