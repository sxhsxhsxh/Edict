/**
 * Created by tarena on 19-6-17.
 */
$(function () {
   var ret_user = false;
   var ret_pw = false;
   var ret_pw1 =false;
   var ret_eml = false;
   var ret_mob = false;
   $("#user").blur(function () {
       if($(this).val()){
           $.ajax({
               url:"/02_regserver",
               type:'post',
               async:true,
               dataType:'json',
               data:{uname:$(this).val()},
               success:function (data) {
                   if (data.status == 1) {
                       $("#hint_user").html("您的用户名可以注册");
                       $("#hint_user").css("color", "green");
                       ret_user = true;
                   } else {
                       $("#hint_user").html("您输入的用户名已存在");
                       $("#hint_user").css("color", "red");
                       ret_user = false;
                  }
              }
          });
       } else {
           $("#hint_user").html("用户名不能为空");
           $("#hint_user").css("color", "red");
           ret_user = false;
       }
   });
   $("#pw").blur(function () {
       var pawre = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,18}$/;
       var upaw = $(this).val();
       if (!pawre.test(upaw)){
           ret_pw = false;
           $(this).next().html("包含数字、字母的6-18位");
           $(this).next().css("color","red");
       }else {
           ret_pw = true;
           $(this).next().html("");
       }
   });
   $("#pw1").blur(function () {
      if($(this).val() == $("#pw").val()){
          ret_pw1 = true;
          $(this).next().html("");
      } else {
          ret_pw1 = false;
          $(this).next().html("密码不一致");
          $(this).next().css("color","red");
      }
   });
   $("#Email").blur(function () {
       var emailre =  /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
       if (emailre.test($(this).val())){
           $(this).next().html("");
           ret_eml = true;
       }else {
           $(this).next().html("您输入的邮箱格式有误,例如xx@xx.com").css("color","red");
           ret_eml = false;
       }
   });
   $("#phone").blur(function () {
       var myreg=/^[1][3,4,5,7,8][0-9]{9}$/;
       var value = $(this).val();
       if (!myreg.test(value)) {
           ret_mob = false;
           $(this).next().html("您输入的手机号有误");
           $(this).next().css("color","red");
       } else {
           ret_mob = true;
           $(this).next().html("");
       }
   });
   $("#btn").click(function () {

      if (ret_user && ret_pw1 && ret_pw && ret_eml && ret_mob){
          $.ajax({
              url:"/02_reg",
              type:'post',
              async:true,
              dataType:'json',
              data:{
                  uname:$("#user").val(),
                  upwd:$("#pw").val(),
                  uemail:$("#Email").val(),
                  utel:$("#phone").val(),
                  active:$("#reading").val()
              },
              succes:function (data) {
                  if(data.status == 1){
                      if(document.referrer==''){
                          $(location).attr('href','/');
                      }
                      else{
                          $(location).attr('href',document.referrer)
                      }
                  }
                  else{alert('注册失败')}
              }
          });
      } else {
          alert("请完善注册信息")
      }
   });
});
