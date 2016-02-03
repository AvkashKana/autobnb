from django.contrib import admin
from guests.models import Reservation, Resident

class ReservationAdmin(admin.ModelAdmin):
    actions = ['promote_to_resident']

    def promote_to_resident(self, request, queryset):
        promoted = []
        skipped = []
        for reso in queryset.all():
            if Resident.objects.filter(was_reso=reso.confirmation_code).exists():
                skipped.append(reso)
                continue
            Resident.objects.create(
                was_reso=reso.confirmation_code,
                thread_id=reso.thread_id,
                is_active=True,
                slug=reso.confirmation_code,
                label="%s from %s" % (reso.name, reso.location),
                picture=reso.picture,
                guest=reso.guest,
                )
            promoted.append(reso)

        self.message_user(request, "Promoted: %s. Skipped: %s." % (promoted, skipped))

    promote_to_resident.short_description = "Promote selected Reservations to Residents"


class ResidentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Resident, ResidentAdmin)
