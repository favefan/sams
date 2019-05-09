// $('#datetimepicker0').datetimepicker();
  // $('#datetimepicker1').datetimepicker();
function sub(sub_btn, sub_form, red_url, rep_url){
    $(sub_btn).click(function() {
        $.ajax({
          type : 'post',
          dataType : 'html',
          url : red_url,
          data : $(sub_form).serialize(),
          contentType : "application/x-www-form-urlencoded",
          success : function(data) {
              alert(data)
              location.replace(rep_url)
          }
        })          
    })
}

