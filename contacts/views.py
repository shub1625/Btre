from django.shortcuts import render,redirect
from .models import Contact
from django.contrib import messages
from django.core.mail import send_mail,EmailMessage

def contact(request):
    """
    Contact inquiry submission
    """
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id,user_id=user_id)
            if has_contacted:
                messages.error(request,'You have already made an inquiry for this listing')
                return redirect('/listings/'+listing_id)

        contact = Contact(listing=listing,listing_id=listing_id,name=name,email=email,
        phone=phone,massage=message,user_id=user_id)

        #Save contact
        contact.save()
        
        #Send Email
        subject = 'Property Listing Inquiry for '+ listing
        body = 'Hey , there has been inquiry for ' + listing + ' By '+ contact.name + ' Please checkout admin panel for more details'
        from_email = 'patneshubham23@gmail.com'
        to_email = [realtor_email,]
        inq_data = 'name : '+name +'\n'+ 'massage : '+ message + '\n' + 'Phone : '+ phone
        email = EmailMessage(subject,body,from_email,to_email)
        email.attach('inquiry.txt', inq_data,'text/plain')

        email.send()
        # send_mail(subject,body,from_email,to_email,fail_silently=False)

        

        messages.success(request,'Your request has been submitted, a realtor will get back to you soon')
        return redirect('/listings/'+listing_id)

    else:
        messages.error(request,'Someting went wrong')
        return redirect('/listings/'+listing_id)
