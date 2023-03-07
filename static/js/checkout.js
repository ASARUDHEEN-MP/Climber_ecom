// $(document).ready(function () {
   
//     $('.paywithrazarpay').click(function (e){
//       e.preventDefault();
//     //    var fname =$("[name='fname']").val();
//     //    var phone=$("[name='phone']").val();
//     //    var email=$("[name='email']").val();
//     //    var phone=$("[name='phone']").val();
//        var token=$("[name='csrfmiddlewaretoken']").val();
      
     
   
     
//         $.ajax({
//             method:"GET",
//             url:"/proceed-to-pay",
//             success:function(response){

//                 // console.log(response);
//                 var options = {
//                     "key": "rzp_test_WcPhXFNsF5Y8XN", // Enter the Key ID generated from the Dashboard
//                     "amount":response.total_price*100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
//                     "currency": "INR",
//                     "name": "Cycles",
//                     "description": "Thank you For Buying with us",
//                     "image": "https://example.com/your_logo",
//                     // "order_id": "order_IluGWxBm9U8zJ8", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
//                     "handler": function (response){
//                             alert(response.razorpay_payment_id);
//                         data ={
//                             "payment_mode":"paid by razorpay",
//                             "payment_id":response.razorpay_payment_id,
//                              csrfmiddlewaretoken:token,
                             
//                         }
//                         $.ajax({
//                             method:"POST",
//                             url:"/placeorder",
//                             success:function(responsec){
//                                 swal("congrz", responsec.status, "success").then((value) => {
//                                     window.location.href='/my_orders'
//                                   });
                               
                                
//                             }
//                         })
                       
//                     },
//                     "prefill": {
//                         "name": "asaru",
//                         "email": "gaurav.kumar@example.com",
//                         "contact": "7989775489",
//                     },
//                     "callback_url": "http://127.0.0.1:8000/pay",
//                     "theme": {
//                         "color": "#3399cc"
//                     }
//                 };
//                 var rzp1 = new Razorpay(options);
//                 rzp1.open();
//             }
         
//             });
      



     
     

     
    
//     });



// });