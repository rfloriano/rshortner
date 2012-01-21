// function Shortener(){
//     var self = this;

//     self.clear = function(){
//         $url.val("");
//         $shortener.val("");
//     }
// }

$(document).ready(function(){
    var $form = $("#id-form-shortener");
    var $table = $("#table-list-url");
    var $url = $("#id_url");
    var $errors = $("#url-errors");
    var $shortener = $("#id-shortener-url");

    $url.val("");
    $shortener.val("");

    $form.submit(function(){
        $.ajax({
            type: 'POST',
            dataType: 'json',
            url: $form.attr("action"),
            data: $form.serialize(),
            success: function(data){
                $("#ul-errors").remove();
                $errors.removeClass("alert-message block-message error");
                if (data.created){
                    $url.val("");
                    var order = ["url", "short_url", "created-at", "page-view"];
                    td = "<tr>";
                    for (o in order){
                        if (order[o] == "short_url"){
                            td += '<td><a href="'+data[order[o]]+'">'+ data[order[o]] +'</a></td>';
                            $shortener.val(data[order[o]]);
                        }else{
                            td += "<td>"+data[order[o]]+"</td>";
                        }
                    }
                    td += "</tr>";
                    $table.prepend(td);
                    $table.find("#default-message").remove();
                    $shortener.select();
                }
                else if (data.short_url == "" && data.errors.url.length > 0){
                    var li = "";
                    for (error in data.errors.url){
                        li += "<li>"+ data.errors.url[error] +"</li>";
                    }
                    $ul = $('<ul id="ul-errors"/>');
                    $ul.append(li);
                    $errors.prepend($ul);
                    $errors.addClass("alert-message block-message error");
                }
            },
            error: function(data){
                $("#ul-errors").remove();
                $errors.removeClass("alert-message block-message error");
                var li = "";
                li += "<li>Você precisa enviar uma URL para encurtar</li>";
                $ul = $('<ul id="ul-errors"/>');
                $ul.append(li);
                $errors.prepend($ul);
                $errors.addClass("alert-message block-message error");
            }
        });
        return false;
    })
});