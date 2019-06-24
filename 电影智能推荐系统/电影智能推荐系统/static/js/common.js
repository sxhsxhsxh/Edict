/**
 * Created by tarena on 19-5-31.
 */
function  createXhr(){
    if(window.XMLHttpRequest){
        var xhr = new XMLHttpRequest();
        return new  XMLHttpRequest();
    }else{
        return new ActiveXobject("Mircrosoft.XmlHTTP")
    }
}




























