$(document).foundation()


function find_today()
{
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth() + 1;
    var yyyy = today.getFullYear();

    var result = {
        "yyyy" : yyyy,
        "mm" : mm,
        "dd" : dd
    };

    return result;
};


function init_date()
{
    $('#the_form')[0].reset();
    
    var today = find_today();
    var dtemp = today.dd.toString();
    var mtemp = today.mm.toString();
    var dd = '0';
    var mm = '0';

    console.log(today);

    if(dtemp < 10)
    { dd += today.dd.toString(); }
    else
    { dd = today.dd.toString(); }

    if(mtemp < 10)
    { mm += today.mm.toString(); }
    else
    { mm = today.mm.toString(); }

    var curDate = today.yyyy.toString() + '-' + mm + '-' + dd;
    console.log(curDate);
    $('#last_date').attr('max', curDate);
};