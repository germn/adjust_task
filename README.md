## Installation

- [Install poetry](https://python-poetry.org/docs/#installation)
- `make install`


## Run API server

- `make run_server`


## URLs from the task

- [Show the number of impressions and clicks that occurred before the 1st of June 2017, broken down by channel and country, sorted by clicks in descending order.](http://localhost:8000/metrics/?group_by=channel&group_by=country&sort_by=-clicks&date_to=2017-06-01) [*]
- [Show the number of installs that occurred in May of 2017 on iOS, broken down by date, sorted by date in ascending order.](http://localhost:8000/metrics/?group_by=date&date_from=2017-05-01&date_before=2017-06-01&os=ios&sort_by=date)
- [Show revenue, earned on June 1, 2017 in US, broken down by operating system and sorted by revenue in descending order.](http://localhost:8000/metrics/?date_before=2017-06-01&country=US&group_by=os&sort_by=-revenue) [**]
- [Show CPI and spend for Canada (CA) broken down by channel ordered by CPI in descending order. Please think carefully which is an appropriate aggregate function for CPI.](http://localhost:8000/metrics/?country=CA&group_by=channel&sort_by=-cpi)

[*] It looks like the hint in the task is incorrect. The hint is for `date <= '2017-06-01'` case. For the specified case `date < '2017-06-01'` [result is different](http://localhost:8000/metrics/?group_by=channel&group_by=country&sort_by=-clicks&date_before=2017-06-01). Or maybe it's just my code incorrect, it's also possible.

[**] Revenue from the day June 1, 2017 itself is not included.


## Notes

- The use-cases imply that we should show only given metrics and "hide" other from output, but the list of API requirements doesn't specify a way to do it. I decided to show all metrics in API output, hope, it's not a big deal.
- More things surely can be done here, including unit tests, better documentation, etc. They were omitted due to time constrains.
- The app was written and tested on Windows 10, Python 3.9.
