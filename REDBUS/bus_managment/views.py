from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import (
    BusForm,
    BusRoutForm,
    BusRouteScheduleForm,
    IntermidiateStopForm,
    BusBookingForm,
    PaymentCancleForm,
    FeedbackForm
)
from .models import BusRoute, BusSchedule, IntermidiateStop, BusBooking, Payment
from django.core.paginator import Paginator
import stripe
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from datetime import datetime, timedelta
from django.db.models import Avg


def home(request):
    if request.user.is_superuser and request.user.is_authenticated:
        payment_details = Payment.objects.filter(payment_status="success")
        payment_details = payment_details.count()
        all_data = BusRoute.objects.all().order_by("id")
        paginator = Paginator(all_data, 5, orphans=1)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(
            request,
            "bus_managment/dashbord.html",
            {"data": page_obj, "count": payment_details},
        )
    else:
        return redirect("home")


def bus(request):
    if request.user.is_superuser and request.user.is_authenticated:
        if request.method == "GET":
            fm = BusForm()
            return render(request, "bus_managment/add_bus.html", {"form": fm})

        if request.method == "POST":
            fm = BusForm(request.POST)
            if fm.is_valid():
                fm.save()
                return redirect("bus_route_add")
    else:
        return redirect("home")


def bus_route(request):
    if request.user.is_superuser and request.user.is_authenticated:
        if request.method == "GET":
            fm = BusRoutForm()
            return render(request, "bus_managment/add_bus_route.html", {"form1": fm})

        if request.method == "POST":
            fm = BusRoutForm(request.POST)
            if fm.is_valid():
                fm.save()
                return redirect("add_bus")
    else:
        return redirect("home")


def update_bus_route(request, id):
    if request.user.is_superuser and request.user.is_authenticated:
        bus_route = get_object_or_404(BusRoute, id=id)

        if request.method == "POST":
            form = BusRoutForm(request.POST, instance=bus_route)
            if form.is_valid():
                form.save()
                return redirect("dashboard")  # Or another redirect after saving
        else:
            form = BusRoutForm(instance=bus_route)

        return render(request, "bus_managment/update_bus_route.html", {"form": form})

    else:
        return redirect("home")


def delete_bus_route(request, id):
    if request.user.is_superuser and request.user.is_authenticated:
        bus_route = get_object_or_404(BusRoute, id=id)

        if request.method == "POST":
            bus_route.delete()
            return redirect("dashboard")

        return render(
            request, "bus_managment/confirm_delete.html", {"bus_route": bus_route}
        )

    else:
        return redirect("home")


def bus_schedule(request):
    if request.user.is_superuser and request.user.is_authenticated:
        if request.method == "POST":
            fm = BusRouteScheduleForm(request.POST)

            if fm.is_valid():
                fm.save()
                return redirect("dashboard")

            else:
                return redirect("bus_schedule")

        else:
            fm = BusRouteScheduleForm()
            return render(request, "bus_managment/bus_schedule.html", {"form": fm})
    else:
        return redirect("home")


def bus_schedule_details(request):
    if request.user.is_superuser and request.user.is_authenticated:
        data = BusSchedule.objects.all()
        bus_schedule_data = []
        for schedule in data:
            # Access the related BusRoute fields
            bus_route = schedule.bus_route_schedule
            sourse = bus_route.sourse
            destinations = bus_route.destinations
            # Retrieve all intermediate stops for this BusRoute
            inter_stops = IntermidiateStop.objects.filter(bus_route=bus_route)

            # Add the relevant data to the list
            bus_schedule_data.append(
                {
                    "schedule": schedule,
                    "sourse": sourse,
                    "destinations": destinations,
                    "inter_stops": inter_stops,
                }
            )

        # all_data = BusRoute.objects.all().order_by('id')
        paginator = Paginator(bus_schedule_data, 5, orphans=1)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        # Pass the data to the template
        return render(
            request,
            "bus_managment/bus_schedul_details.html",
            {
                "bus_schedule_data": page_obj,
            },
        )
    else:
        return redirect("home")


def update_schedule(request, id):
    if request.user.is_superuser and request.user.is_authenticated:
        bus_schedule = get_object_or_404(BusSchedule, id=id)
        if request.method == "POST":
            form = BusRouteScheduleForm(request.POST, instance=bus_schedule)
            if form.is_valid():
                form.save()
                return redirect(
                    "bus_schedule_details"
                )  # Redirect to the schedule list page
        else:
            form = BusRouteScheduleForm(instance=bus_schedule)
        return render(request, "bus_managment/update_schedule.html", {"form": form})

    else:
        return redirect("home")


def delete_schedule(request, id):
    if request.user.is_superuser and request.user.is_authenticated:
        bus_schedule = get_object_or_404(BusSchedule, id=id)
        bus_schedule.delete()
        return redirect("bus_schedule_details")

    else:
        return redirect("home")


def intermidiate_stop(request):
    if request.method == "GET":
        fm = IntermidiateStopForm()
        return render(request, "bus_managment/intermidiate.html", {"form": fm})

    if request.method == "POST":
        fm = IntermidiateStopForm(request.POST)
        if fm.is_valid():
            fm.save()
            return redirect("intermidiate")
        else:
            return redirect("dashboard")


def show_bus_details(request, id):

    bus_schedule = get_object_or_404(BusSchedule, id=id)
    available_seats = bus_schedule.avalable_seates

    return render(request, "bus_details.html", {"bus": bus_schedule})


def book_ticket(request, id):
    data = get_object_or_404(BusSchedule, id=id)
    available_seats = data.avalable_seates
    if request.user.is_authenticated:
        if request.method == "POST":
            book_data = BusBookingForm(request.POST)
            if book_data.is_valid():
                bus_data = book_data.save(commit=False)
                bus_data.user = request.user
                bus_data.bus_schedule = data
                bus_data.save()
                seats = int(request.POST["seats"])
                data.avalable_seates -= seats
                data.save()
                # booking_data = request.POST
                pay_ammount = seats * data.tickit_price
                return render(
                    request,
                    "checkout.html",
                    {
                        "data": bus_data,
                        "pay_ammount": pay_ammount,
                        "bus_schedule_data": data,
                    },
                )
            else:
                return render(
                    request,
                    "bus_managment/bus_booking.html",
                    {"form": book_data, "seats_range": range(available_seats)},
                )
        else:
            fm = BusBookingForm()
            context = {
                "form": fm,
                "seats_range": range(
                    1, available_seats + 1
                ),  # Use range for looping in template
            }
            return render(request, "bus_managment/bus_booking.html", context)
    else:
        return redirect("login")


stripe.api_key = settings.STRIPE_SECRET_KEY


def create_session(request, id):
    data = get_object_or_404(BusBooking, id=id)
    if request.method == "POST":
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "inr",
                            "product_data": {
                                "name": "Bus Ticket",
                            },
                            "unit_amount": int(request.POST["ammount"]) * 100,
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url=f"http://127.0.0.1:8000/bus_managment/success_session/{data.id}/",
                cancel_url=f"http://127.0.0.1:8000/bus_managment/cencle_session/{data.id}/",
            )
            return redirect(session.url, code=303)  # Redirect user to Stripe Checkout
        except Exception as e:
            return JsonResponse({"error": str(e)})


def cencle_session(request, id):
    data = get_object_or_404(BusBooking, id=id)
    bus_schedule_id = data.bus_schedule.id
    bus_schedule_data = get_object_or_404(BusSchedule, id=bus_schedule_id)
    bus_schedule_data.avalable_seates = bus_schedule_data.avalable_seates + data.seats
    bus_schedule_data.save()
    data.payment_status = "cancle"
    data.save()

    subject = data.customer_name
    total_seats = data.seats
    payment = data.bus_schedule.tickit_price
    total_payment = total_seats * payment
    message = f" Hii {data.customer_name} Your booking is  incompleted! you are book {data.seats} seats and Painding amoount is {total_payment} Bus name {data.bus_schedule.bus.bus_name}({data.bus_schedule.bus.bus_type})"
    address = data.customer_email
    if address and subject and message:
        send_mail(subject, message, settings.EMAIL_HOST_USER, [address])
    # return render(request, 'cencle_book.html')
    return redirect("home")


def success_session(request, id):
    data = get_object_or_404(BusBooking, id=id)
    data.payment_status = "success"
    data.save()
    context = {}
    subject = data.customer_name
    total_seats = data.seats
    payment = data.bus_schedule.tickit_price
    total_payment = total_seats * payment
    message = f" Hii {data.customer_name} Your booking is successfully Completed! you are book {data.seats} seats and Paid amoount is {total_payment} Bus name {data.bus_schedule.bus.bus_name}({data.bus_schedule.bus.bus_type})"
    address = data.customer_email
    if address and subject and message:
        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, [address])
            context["result"] = "Email sent successfully"
        except Exception as e:
            context["result"] = f"Error sending email: {e}"
    else:
        context["result"] = "All fields are required"

    return render(
        request,
        "success_book.html",
        {"data": data, "context": context, "total_payment": total_payment},
    )


def booking_history(request):
    user = request.user
    data = BusBooking.objects.all()
    booking_list = []
    for data in data:
        if data.user.username == user.username:
            booking_list.append(data)
    paginator = Paginator(booking_list, 10, orphans=2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "booking_history.html", {"data": page_obj})


def history_delete(request, id):
    history_data = get_object_or_404(BusBooking, id=id)
    history_data.delete()
    return redirect("booking_history")


def ticket_cancle(request, id):
    data = get_object_or_404(BusBooking, id=id)

    if request.method == "GET":
        if data.payment_status == "success":
            fm = PaymentCancleForm()
            return render(request, "payment_cancle_form.html", {"data": fm})
        messages.error(request, "You cannot cancel this ticket.")
        return redirect("booking_history")

    if request.method == "POST":
        cancellation_data = PaymentCancleForm(request.POST)
        if cancellation_data.is_valid():
            bus_departure_time = data.bus_schedule.department_time  # time object
            bus_departure_datetime = datetime.combine(
                datetime.today(), bus_departure_time
            )

            cancellation_request_time_str = request.POST["cancellation_date"]
            cancellation_request_time = datetime.strptime(
                cancellation_request_time_str, "%Y-%m-%dT%H:%M"
            )

            two_hours_before_departure = bus_departure_datetime - timedelta(hours=2)
            # breakpoint()

            if cancellation_request_time < two_hours_before_departure:

                data.payment_status = "refund"
                data.bus_schedule.avalable_seates += data.seats
                data.save()
                cancellation = cancellation_data.save(commit=False)
                cancellation.payment_status = "refund"
                cancellation.bus_booking = data
                cancellation.save()
                subject = data.customer_name
                total_seats = data.seats
                payment = data.bus_schedule.tickit_price
                total_payment = total_seats * payment
                message = f" Hii {data.customer_name} Your booking is  incompleted! you are book {data.seats} seats and Painding amoount is {total_payment} Bus name {data.bus_schedule.bus.bus_name}({data.bus_schedule.bus.bus_type})"
                address = data.customer_email
                if address and subject and message:
                    send_mail(subject, message, settings.EMAIL_HOST_USER, [address])

                messages.success(
                    request,
                    "Your cancellation was successfully submitted and all information are send mention email address.",
                )
                return redirect("booking_history")
            else:

                messages.warning(
                    request,
                    "Cancellation request needs admin approval (within 2 hours of departure).",
                )
                cancellation = cancellation_data.save(commit=False)
                cancellation.bus_booking = data
                cancellation.save()
                return redirect("booking_history")

        messages.error(request, "Your cancellation form was not submitted.")
        return redirect("booking_history")


def cancle_request_details(request):
    payment_details = Payment.objects.all()

    return render(
        request, "payment_cancellation_details.html", {"details": payment_details}
    )


def cancellation_approval(request, id):
    if request.user.is_superuser and request.user.is_authenticated:
        data = get_object_or_404(Payment, id=id)

        action = request.POST["Action"]
        if action == "accept":

            boking_seats = data.bus_booking.seats
            ticket_price = data.bus_booking.bus_schedule.tickit_price
            total_ammount = boking_seats * ticket_price
            bus_schedule_data = get_object_or_404(
                BusSchedule, id=data.bus_booking.bus_schedule.id
            )
            # manage bus_schedule seats

            bus_schedule_data.avalable_seates += data.bus_booking.seats
            bus_schedule_data.save()
            # bus_booking  payment status manage

            bus_booking_data = get_object_or_404(BusBooking, id=data.bus_booking.id)
            bus_booking_data.payment_status = "refund"
            bus_booking_data.save()
            # payment status manag

            data.payment_status = "refund"
            data.save()
            user_name = data.bus_booking.customer_name
            user_email = data.bus_booking.customer_email
            masseges = f"Hii {user_name} your cancellation requset are accept in and your total ammount is {total_ammount} are refund your bank account within Two days Thank You!"
            send_mail(user_name, masseges, settings.EMAIL_HOST_USER, [user_email])
            return redirect("cancellation_details")

        elif action == "reject":
            data.payment_status = "cancle"
            data.save()
            user_name = data.bus_booking.customer_name
            user_email = data.bus_booking.customer_email
            masseges = f"Hii {user_name} your cancellation requset are not accepted!"
            send_mail(user_name, masseges, settings.EMAIL_HOST_USER, [user_email])
            return redirect("cancellation_details")


def feedback(request, id):
    if request.method == 'POST':
        # Get the BusBooking object
        data = get_object_or_404(BusBooking, id=id)
        bus_schedule_id = data.bus_schedule.id
        bus_schedule_data = get_object_or_404(BusSchedule, id = bus_schedule_id)
        
        # Instantiate the form with POST data
        form = FeedbackForm(request.POST)
        # Check if form is valid
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user  # Attach the user who is submitting the feedback
            feedback.booking = data   
            feedback.bus_schedule = bus_schedule_data # Link the feedback to the specific booking
            feedback.save()              # Save the feedback

            messages.success(request, 'Thank you for giving feedback!')
            return redirect('booking_history')
        else:
            # Print the form errors for debugging in the server console
            print(form.errors)

            messages.error(request, 'Your feedback was not submitted. Please try again!')
            return redirect('booking_history')

    else:
        # If the method is GET, render the form
        fm = FeedbackForm()
        return render(request, 'feedback.html', {'form': fm})