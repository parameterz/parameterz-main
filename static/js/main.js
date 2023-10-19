// session storage stuff 
function setStorage(item) {
  //get the input data
  if (item.value) {
      // and save to sessionStorage
      window.sessionStorage[item.id] = item.value;
  }
  return item;
}//end setStorage
function getStorage (item) {
  var storage = window.sessionStorage;
  if (!storage) return;// the browser does not support storage
  //if the sessionStorage key exists, load the value in the appropriate input
  if (storage[item]) {
      $('#' + item).val(storage[item]);
  } else {
      return;
  }
}//end getStorage

//Patient biz
function Patient(params) {
    //accepts params as an object literal
    //otherwise, the Patient properties can be assigned later
    params = params || {};
    for (var p in params) {
        this[p] = params[p];
    }
}
Patient.prototype.bmi = function () {
    if (this.ht && this.wt) {
        //requires ht in cm; wt in kg
        return this.wt / Math.pow((this.ht / 100), 2);
    } else {
        return undefined;
    }
};
Patient.prototype.bsa = function (method) {
    method = method.toLowerCase() || 'haycock';
    if (this.ht && this.wt) {
        var
        ht = this.ht,
            wt = this.wt;
        //requires ht in cm; wt in kg
        switch (method) {
        case "dubois":
            return 0.007184 * Math.pow(ht, 0.725) * Math.pow(wt, 0.425);
        case "haycock":
            return 0.024265 * Math.pow(ht, 0.3964) * Math.pow(wt, 0.5378);
        case "gehan":
            return 0.0235 * Math.pow(ht, 0.42246) * Math.pow(wt, 0.51456);
        case "mosteller":
            return Math.sqrt((ht * wt) / 3600);
        case "boyd":
            wt = wt * 1000;
            var exponent = 0.7285 - 0.0188 * (Math.LOG10E * Math.log(wt)); //necessary to get the Log base 10 of (wt) 10of (wt)
            return 0.0003207 * Math.pow(ht, 0.3) * Math.pow(wt, exponent);
        case "dreyer":
            return 0.1 * Math.pow(wt, (2 / 3));
        default:
            // returns Haycock in the event an unfamiliar method is passed in
            return 0.024265 * Math.pow(ht, 0.3964) * Math.pow(wt, 0.5378);
        } //end switch
    } else {
        return undefined;
    }
}; //end bsa function
Patient.prototype.getAge = function (s) {
    //TODO
    //return age in requested format from the property pt.age, which is always in YEARS
};

$(document).ready(function() {
    //reset data when reset button is clicked
    $('form').bind('reset', function() {
        $('.zscore, .range').html('');
        window.sessionStorage.clear();
    });
    // updated derived elemets
    updateDerivedElements();
});

function ColorizeZ(x_in) {
    //converts  a z-score (passed in as 'x_in')
    //to a HUE to use in HSL color scheme
    // z = 0 = Green (hue = 120)
    // z = 1.65 = Yellow (hue = 60)
    // z >= 5 = Red (hue = 0)
    //Polynomial_Quadratic_model
    // To the best of my knowledge this code is correct.
    // If you find any errors or problems please contact
    // me directly using zunzun@zunzun.com.
    //      James
    //
    x_in = math.abs(x_in);
    //keep x from scaling beyond 5
    if (x_in > 5 ) {
        x_in = 5;
    }
    var temp;
    temp = 0.0;

    // coefficients
    var a = -6.4940794865907948E-14;
    var b = 4.2453188602442310E+01;
    var c = -3.6906377204884606E+00;

    temp += a + b * x_in + c * Math.pow(x_in, 2.0);
    
    return 120.0 - temp;

}

function updateDerivedElements() {
    //handles updating things like fractional shortening, lv mass, e/a ratios, etc
    //that are calculated(derived) based on other direct measurements
    //  1. ensure all the required elements exist, as needed
    //  2. put calculated value in the derived input
    //  3. update element to get z-score, ranges
    
    /*     RV FAC A4C     */
    $('#rv_eda_a4c, #rv_esa_a4c').change(function(){
        var fac;
        fac = ( $('#rv_eda_a4c').val() - $('#rv_esa_a4c').val() ) / $('#rv_eda_a4c').val();
        if ( !isNaN(fac) && $('#rv_fac_a4c').length ) {
            $('#rv_fac_a4c').val(Math.round(fac * 100)).change();
        }
    });    

        
    /*     RV FAC 3C     */
    $('#rv_eda_3c, #rv_esa_3c').change(function(){
        var fac;
        fac = ( $('#rv_eda_3c').val() - $('#rv_esa_3c').val() ) / $('#rv_eda_3c').val();
        if ( !isNaN(fac) && $('#rv_fac_3c').length ) {
            $('#rv_fac_3c').val(Math.round(fac * 100)).change();
        }
    });    

    
    /*    RV FAC 'GLOBAL'    */
    if($('#rv_fac_global').length){
        $('#rv_fac_3c, #rv_fac_a4c').change(function(){
            var fac;
            fac = ( parseFloat($('#rv_fac_3c').val()) + parseFloat($('#rv_fac_a4c').val()) ) / 2;
            if ( !isNaN(fac) ) {
                $('#rv_fac_global').val(Math.round(fac)).change();
            }
    });
    }
    

    /*    RV Peak Long. Strain    */
    if($('#rv_pls_global').length){
        $('#rv_pls_a4c, #rv_pls_3c').change(function(){
            var pls;
            pls = ( parseFloat($('#rv_pls_a4c').val()) + parseFloat($('#rv_pls_3c').val()) ) / 2;
            if ( !isNaN(pls) ) {
                $('#rv_pls_global').val(Math.round(pls)).change();
                }
        });
    }
    
    /*    TV E/A Ratio    */
    if($('#tv_e').length && $('#tv_a').length && $('#tv_ea_ratio').length){
        $('#tv_e, #tv_a').change(function(){
            var ratio;
            ratio =  parseFloat($('#tv_e').val()) / parseFloat($('#tv_a').val()) ;
            if ( !isNaN(ratio) ) {
                $('#tv_ea_ratio').val(ratio.toFixed(2)).change();
                }
        });
    }

    /*    RV TDI E/A Ratio    */
    if($('#rv_tdi_e').length && $('#rv_tdi_a').length && $('#rv_tdi_ea_ratio').length){
        $('#rv_tdi_e, #rv_tdi_a').change(function(){
            var ratio;
            ratio =  parseFloat($('#rv_tdi_e').val()) / parseFloat($('#rv_tdi_a').val()) ;
            if ( !isNaN(ratio) ) {
                $('#rv_tdi_ea_ratio').val(ratio.toFixed(2)).change();
                }
        });
    }
    
    /*    TV E/e' Ratio    */
    if($('#rv_tdi_e').length && $('#tv_e').length && $('#tv_Ee_ratio').length){
        $('#rv_tdi_e, #tv_e').change(function(){
            var ratio;
            ratio =  parseFloat($('#tv_e').val()) / parseFloat($('#rv_tdi_e').val()) ;
            if ( !isNaN(ratio) ) {
                $('#tv_Ee_ratio').val(ratio.toFixed(2)).change();
                }
        });
    } 
    
    
} //end updated_derived_elements fx