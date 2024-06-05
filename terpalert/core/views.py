from django.shortcuts import render, redirect
from accounts.models import DailyMenu, Menu
from django.http import JsonResponse
from datetime import date


def home(request):
    """
    Renders the website landing page
    """
    return render(request, 'index.html')


def check_for_alert(request):
    """
    Handle the Ajax request to check if an item is in DailyMenu table for today's date

    :return: JsonResponse with fields "found", "item", and "dining_halls" (if found is true)
    """
    if 'item' in request.GET:
        item = request.GET['item']

        menu_item = Menu.objects.get(item=item)  # Get Menu object for that item
        daily_menu_item = DailyMenu.objects.filter(menu_item_id=menu_item.id, date=date.today())

        if daily_menu_item.exists():
            # Item is being served today
            data = {'found': True, 'item': item}

            # Add dining halls the item is applicable to
            dining_halls = []
            if daily_menu_item[0].yahentamitsi_dining_hall:
                dining_halls.append('Yahentamitsi')
            if daily_menu_item[0].south_dining_hall:
                dining_halls.append('South')
            if daily_menu_item[0].two_fifty_one_dining_hall:
                dining_halls.append('251')

            data['dining_halls'] = ', '.join(dining_halls)
        else:
            # Item isn't being served today
            data = {'found': False, 'item': item}

        return JsonResponse(data)
    else:
        return redirect('home')
