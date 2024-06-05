from django.shortcuts import render, redirect
from accounts.models import DailyMenu, Menu
from django.http import HttpResponse, JsonResponse
from datetime import date


def home(request):
    return render(request, 'index.html')


def check_for_alert(request):
    if 'item' in request.GET:
        item = request.GET['item']

        menu_item = Menu.objects.get(item=item)  # Get Menu object for that item
        daily_menu_item = DailyMenu.objects.filter(menu_item_id=menu_item.id, date=date.today())

        if daily_menu_item.exists():
            data = {'found': True, 'item': item}

            # Add dining halls the alert is applicable to
            dining_halls = []
            if daily_menu_item[0].yahentamitsi_dining_hall:
                dining_halls.append('Yahentamitsi')
            if daily_menu_item[0].south_dining_hall:
                dining_halls.append('South')
            if daily_menu_item[0].two_fifty_one_dining_hall:
                dining_halls.append('251')

            data['dining_halls'] = ', '.join(dining_halls)
        else:
            data = {'found': False, 'item': item}

        return JsonResponse(data)
    else:
        return redirect('home')
