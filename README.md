# NHS Delayed Transfers of Care

This project analyses regional differences in delayed transfers of care (DTOC). A DTOC occurs when a patient is ready to leave the hospital, but their discharge is delayed - often because they are awaiting transfer to another care provider (e.g., residential home, community hospice etc.)
Delayed transfers of care are generally viewed as negative for both the patient's outcome and the smooth functioning of the healthcare system as a whole, as less beds will be available for incoming patients.

For more information, see:
https://www.bbc.co.uk/news/uk-england-39258606
https://www.kingsfund.org.uk/publications/delayed-transfers-care-quick-guide

## Dataset
Total numbers of 'delayed days' for each local authority region are published every month by NHS England, and these monthly situation reports are available from 2010-2020, and can be downloaded here:
https://www.england.nhs.uk/statistics/statistical-work-areas/delayed-transfers-of-care/

Use 'scrapeNHS_dtoc.py' to download all the monthly datasets from NHS England.
Then use 'dtoc_dataset.py' to standardise and combine files into one large dataset, and a smaller summary dataset 'dtoc_totals.csv'.

## Visualisation
The script 'dtoc.py' uses dtoc_totals.csv to visualise the differences in delayed transfers across time, and across regions of England.

For instance, we can produce a line graph of average delays in transfers over the last decade:

![alt text](https://github.com/JonnyP1990/dtoc/blob/main/Plots/dtocXtime3.png?raw=true)

And we can visualise regional differences in the total number of delayed days across this period using a map plot: 

![alt text](https://github.com/JonnyP1990/dtoc/blob/main/Plots/dtoc_totals.png?raw=true)


To create the map plot, the regional area codes are included in the file 'regionIDs.csv', and the regional shape geoJSON file can be downloaded from the ONS here:
https://geoportal.statistics.gov.uk/search?collection=Dataset&sort=name&tags=all(BDY_CTYUA)


