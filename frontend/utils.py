from django.http import JsonResponse


def password_checker(password):
    SpecialSym = ['$', '@', '#', '%']
    val = True

    if len(password) < 8:
        return JsonResponse({'statusMsg': 'length should be at least 8'}, status=404)

    if len(password) > 15:
        return JsonResponse({'statusMsg': 'length should be not be greater than 15'}, status=404)

    if not any(char.isdigit() for char in password):
        return JsonResponse({'statusMsg': 'Password should have at least one numeral'}, status=404)

    if not any(char.isupper() for char in password):
        return JsonResponse({'statusMsg': 'Password should have at least one uppercase letter'}, status=404)

    if not any(char.islower() for char in password):
        return JsonResponse({'statusMsg': 'Password should have at least one lowercase letter'}, status=404)

    if not any(char in SpecialSym for char in password):
        return JsonResponse({'statusMsg': 'Password should have at least one of the symbols $@#'}, status=404)
    if val:
        return val
