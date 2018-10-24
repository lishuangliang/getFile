/**
 * Created by tarena on 18-10-23.
 */

(function (win, doc) {

    win.lsl = win.lsl || {};

    //写cookies
lsl.setCookie = function setCookie(c_name, value, expiredays){
　　 var exdate=new Date();
　　 exdate.setDate(exdate.getDate() + expiredays);
　　 document.cookie=c_name+ "=" + escape(value) + ((expiredays==null) ? "" : ";expires="+exdate.toGMTString());
}

//读取cookies
lsl.getCookie = function getCookie(name) {
    var arr,reg=new RegExp("(^| )"+name+"=([^;]*)(;|$)");
    if(arr=document.cookie.match(reg))
        return (arr[2]);
    return null;
}

//删除cookies
lsl.delCookie = function delCookie(name) {
    var exp = new Date();
    exp.setTime(exp.getTime() - 1);
    var cval=getCookie(name);
    if(cval!=null) document.cookie= name + "="+cval+";expires="+exp.toGMTString();
}



})(window, document);