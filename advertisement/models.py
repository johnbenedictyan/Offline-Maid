import math
from datetime import date, datetime, timedelta

from agency.models import Agency
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
# from onlinemaid.storage_backends import PublicMediaStorage


class QuarterChoices(models.TextChoices):
    ONE = '1', _('First Quarter')
    TWO = '2', _('Second Quarter')
    THREE = '3', _('Third Quarter')
    FOUR = '4', _('Fourth Quarter')


class YearChoices(models.TextChoices):
    TWENTY_TWENTY_ONE = '2021', _('2021')
    TWENTY_TWENTY_TWO = '2022', _('2022')
    TWENTY_TWENTY_THREE = '2023', _('2023')
    TWENTY_TWENTY_FOUR = '2024', _('2024')
    TWENTY_TWENTY_FIVE = '2025', _('2025')


class AdvertisementLocation(models.Model):
    name = models.CharField(
        verbose_name=_('Page name'),
        max_length=30
    )

    stripe_price_id = models.CharField(
        verbose_name=_('Advertisement Stripe ID'),
        max_length=255,
        null=True
    )

    total_amount_allowed = models.PositiveSmallIntegerField(
        verbose_name=_('Total number of allowed advertisements per quarter'),
        default=5
    )

    price = models.PositiveSmallIntegerField(
        verbose_name=_('Price'),
        default=0
    )

    active = models.BooleanField(
        default=True
    )

    def get_current_quarter(self):
        return (datetime.now().month - 1) // 3 + 1

    def get_current_year(self):
        return datetime.now().year

    def get_slots(self):
        if self.get_current_year() == 2021:
            year_choice = YearChoices.TWENTY_TWENTY_ONE
            next_year_choice = YearChoices.TWENTY_TWENTY_TWO
        elif self.get_current_year() == 2022:
            year_choice = YearChoices.TWENTY_TWENTY_TWO
            next_year_choice = YearChoices.TWENTY_TWENTY_THREE
        elif self.get_current_year() == 2023:
            year_choice = YearChoices.TWENTY_TWENTY_THREE
            next_year_choice = YearChoices.TWENTY_TWENTY_FOUR
        elif self.get_current_year() == 2024:
            year_choice = YearChoices.TWENTY_TWENTY_FOUR
            next_year_choice = YearChoices.TWENTY_TWENTY_FIVE

        if self.get_current_quarter == 1:
            q1_ads = self.advertisements.filter(
                quarter=QuarterChoices.ONE,
                year=year_choice
            ).count()
            q2_ads = self.advertisements.filter(
                quarter=QuarterChoices.TWO,
                year=year_choice
            ).count()
            q3_ads = self.advertisements.filter(
                quarter=QuarterChoices.THREE,
                year=year_choice
            ).count()
            q4_ads = self.advertisements.filter(
                quarter=QuarterChoices.FOUR,
                year=year_choice
            ).count()
            return [
                [
                    self.total_amount_allowed - q1_ads,
                    "Q1 " + year_choice,
                    q1_ads >= self.total_amount_allowed,
                    "q1-" + year_choice
                ],
                [
                    self.total_amount_allowed - q2_ads,
                    "Q2 " + year_choice,
                    q2_ads >= self.total_amount_allowed,
                    "q2-" + year_choice
                ],
                [
                    self.total_amount_allowed - q3_ads,
                    "Q3 " + year_choice,
                    q3_ads >= self.total_amount_allowed,
                    "q3-" + year_choice
                ],
                [
                    self.total_amount_allowed - q4_ads,
                    "Q4 " + year_choice,
                    q4_ads >= self.total_amount_allowed,
                    "q4-" + year_choice
                ]
            ]
        elif self.get_current_quarter == 2:
            q2_ads = self.advertisements.filter(
                quarter=QuarterChoices.TWO,
                year=year_choice
            ).count()
            q3_ads = self.advertisements.filter(
                quarter=QuarterChoices.THREE,
                year=year_choice
            ).count()
            q4_ads = self.advertisements.filter(
                quarter=QuarterChoices.FOUR,
                year=year_choice
            ).count()
            next_q1_ads = self.advertisements.filter(
                quarter=QuarterChoices.ONE,
                year=next_year_choice
            ).count()
            return [
                [
                    self.total_amount_allowed - q2_ads,
                    "Q2 " + year_choice,
                    q2_ads >= self.total_amount_allowed,
                    "q2-" + year_choice
                ],
                [
                    self.total_amount_allowed - q3_ads,
                    "Q3 " + year_choice,
                    q3_ads >= self.total_amount_allowed,
                    "q3-" + year_choice
                ],
                [
                    self.total_amount_allowed - q4_ads,
                    "Q4 " + year_choice,
                    q4_ads >= self.total_amount_allowed,
                    "q4-" + year_choice
                ],
                [
                    self.total_amount_allowed - next_q1_ads,
                    "Q1 " + next_year_choice,
                    next_q1_ads >= self.total_amount_allowed,
                    "q1-" + next_year_choice
                ]
            ]
        elif self.get_current_quarter == 3:
            q3_ads = self.advertisements.filter(
                quarter=QuarterChoices.THREE,
                year=year_choice
            ).count()
            q4_ads = self.advertisements.filter(
                quarter=QuarterChoices.FOUR,
                year=year_choice
            ).count()
            next_q1_ads = self.advertisements.filter(
                quarter=QuarterChoices.ONE,
                year=next_year_choice
            ).count()
            next_q2_ads = self.advertisements.filter(
                quarter=QuarterChoices.TWO,
                year=next_year_choice
            ).count()
            return [
                [
                    self.total_amount_allowed - q3_ads,
                    "Q3 " + year_choice,
                    q3_ads >= self.total_amount_allowed,
                    "q3-" + year_choice
                ],
                [
                    self.total_amount_allowed - q4_ads,
                    "Q4 " + year_choice,
                    q4_ads >= self.total_amount_allowed,
                    "q4-" + year_choice
                ],
                [
                    self.total_amount_allowed - next_q1_ads,
                    "Q1 " + next_year_choice,
                    next_q1_ads >= self.total_amount_allowed,
                    "q1-" + next_year_choice
                ],
                [
                    self.total_amount_allowed - next_q2_ads,
                    "Q2 " + next_year_choice,
                    next_q2_ads >= self.total_amount_allowed,
                    "q2-" + next_year_choice
                ]
            ]
        else:
            q4_ads = self.advertisements.filter(
                quarter=QuarterChoices.FOUR,
                year=year_choice
            ).count()
            next_q1_ads = self.advertisements.filter(
                quarter=QuarterChoices.ONE,
                year=next_year_choice
            ).count()
            next_q2_ads = self.advertisements.filter(
                quarter=QuarterChoices.TWO,
                year=next_year_choice
            ).count()
            next_q3_ads = self.advertisements.filter(
                quarter=QuarterChoices.THREE,
                year=next_year_choice
            ).count()
            return [
                [
                    self.total_amount_allowed - q4_ads,
                    "Q4 " + year_choice,
                    q4_ads >= self.total_amount_allowed,
                    "q4-" + year_choice
                ],
                [
                    self.total_amount_allowed - next_q1_ads,
                    "Q1 " + next_year_choice,
                    next_q1_ads >= self.total_amount_allowed,
                    "q1-" + next_year_choice
                ],
                [
                    self.total_amount_allowed - next_q2_ads,
                    "Q2 " + next_year_choice,
                    next_q2_ads >= self.total_amount_allowed,
                    "q2-" + next_year_choice
                ],
                [
                    self.total_amount_allowed - next_q3_ads,
                    "Q3 " + next_year_choice,
                    next_q3_ads >= self.total_amount_allowed,
                    "q3-" + next_year_choice
                ]
            ]

    def get_name(self):
        if self.name == 'featured_maids_ad':
            return "Featured Maids Advertisement"
        else:
            return self.name.replace("_", " ").replace("ad", "Page Advertisement").title()

    def set_purge(self):
        purgeable_ad_requests = [
            x for x in self.advertisements if x.is_purgeable()
        ]
        for ad in purgeable_ad_requests:
            ad.delete()

    def __str__(self) -> str:
        return self.get_name() + ' - ' + 'Active' if self.active else 'Inactive'


class Advertisement(models.Model):
    agency = models.ForeignKey(
        Agency,
        on_delete=models.CASCADE,
        related_name='advertisements'
    )

    location = models.ForeignKey(
        AdvertisementLocation,
        on_delete=models.CASCADE,
        related_name='advertisements'
    )

    quarter = models.CharField(
        max_length=1,
        choices=QuarterChoices.choices,
        default=QuarterChoices.ONE
    )

    year = models.CharField(
        max_length=4,
        choices=YearChoices.choices,
        default=YearChoices.TWENTY_TWENTY_ONE
    )

    approved = models.BooleanField(
        verbose_name=_('Approved'),
        default=False,
        editable=False
    )

    paid = models.BooleanField(
        verbose_name=_('Paid'),
        default=False,
        editable=False
    )

    price_paid = models.PositiveSmallIntegerField(
        verbose_name=_('Price Paid'),
        default=0
    )

    time_created = models.DateTimeField(
        default=timezone.now
    )

    def get_current_quarter(self):
        return (datetime.now().month - 1) // 3 + 1

    def get_current_year(self):
        return datetime.now().year

    def get_price(self):
        year = datetime.now().year
        q1_start = date(year, 1, 1)
        q2_start = date(year, 4, 1)
        q3_start = date(year, 7, 1)
        q4_start = date(year, 10, 1)
        next_q1_start = date(year + 1, 1, 1)

        today = date.today()
        q1_frac = 1 - (today - q1_start).days / (q2_start - q1_start).days
        q2_frac = 1 - (today - q2_start).days / (q3_start - q2_start).days
        q3_frac = 1 - (today - q3_start).days / (q4_start - q3_start).days
        q4_frac = 1 - (today - q4_start).days / (next_q1_start - q4_start).days

        if not self.paid:
            if str(self.get_current_year()) < self.year:
                return self.location.price * 100
            else:
                current_quarter = self.get_current_quarter()
                if current_quarter == 1:
                    if self.quarter == QuarterChoices.ONE:
                        return math.ceil(q1_frac * self.location.price * 100)
                    else:
                        return self.location.price
                elif current_quarter == 2:
                    if self.quarter == QuarterChoices.TWO:
                        return math.ceil(q2_frac * self.location.price * 100)
                    else:
                        return self.location.price
                elif current_quarter == 3:
                    if self.quarter == QuarterChoices.THREE:
                        return math.ceil(q3_frac * self.location.price * 100)
                    else:
                        return self.location.price
                else:
                    if self.quarter == QuarterChoices.FOUR:
                        return math.ceil(q4_frac * self.location.price * 100)
                    else:
                        return self.location.price * 100

    def get_formatted_price(self):
        return self.get_price() / 100

    def get_quarter_start(self):
        today = date.today()
        if self.quarter == QuarterChoices.ONE:
            q1_start = date(int(self.year), 1, 1)
            return today if today > q1_start else q1_start
        elif self.quarter == QuarterChoices.TWO:
            q2_start = date(int(self.year), 4, 1)
            return today if today > q2_start else q2_start
        elif self.quarter == QuarterChoices.THREE:
            q3_start = date(int(self.year), 7, 1)
            return today if today > q3_start else q3_start
        elif self.quarter == QuarterChoices.FOUR:
            q4_start = date(int(self.year), 10, 1)
            return today if today > q4_start else q4_start

    def get_quarter_end(self):
        year = datetime.now().year
        q1_end = date(year, 4, 1) - timedelta(days=1)
        q2_end = date(year, 7, 1) - timedelta(days=1)
        q3_end = date(year, 10, 1) - timedelta(days=1)
        q4_end = date(year + 1, 1, 1) - timedelta(days=1)

        if self.quarter == QuarterChoices.ONE:
            return q1_end

        elif self.quarter == QuarterChoices.TWO:
            return q2_end

        elif self.quarter == QuarterChoices.THREE:
            return q3_end

        elif self.quarter == QuarterChoices.FOUR:
            return q4_end

    def get_created_duration(self):
        return (datetime.now() - self.time_created).total_seconds()

    def get_name(self):
        return self.location.get_name() + " - Q" + self.quarter + " " +self.year

    def set_paid(self):
        self.paid = True
        self.save()

    def set_price_paid(self, price_paid):
        self.price_paid = price_paid
        self.save()

    def is_purgeable(self):
        return not self.paid and self.get_created_duration() > 1000

    def provision_feat_maid_ad(self):
        if self.location.name == 'featured_maids_ad':
            self.agency.increment_featured_fdw(1)

    # photo = models.FileField(
    #     verbose_name=_('Advertisement Photo'),
    #     null=True,
    #     storage=PublicMediaStorage()
    # )

    # remarks = models.TextField(
    #     verbose_name=_('Testimonial statment'),
    #     null=True
    # )

    # frozen = models.BooleanField(
    #     default=False,
    #     editable=False
    # )

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.time_created = timezone.now()
        return super().save(*args, **kwargs)
