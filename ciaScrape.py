import os
import requests
import bs4 as bs
import csv
import re

with open("cleanCountries.csv") as csvfileA:
    reader = csv.DictReader(csvfileA)
    with open('countryData.csv', 'a') as csvfileB:
        fieldnames = ['Region',
                      'Code',
                      'Short Name',
                      'Long Name',
                      'Population',
                      'Population Growth Rate',
                      'GDP (PPP)',
                      'GDP per Capita',
                      'Real GDP Growth Rate',
                      'Gross National Savings',
                      'Labor Force',
                      'Unemployment Rate',
                      'Population below poverty line',
                      'Inflation Rate',
                      'Commerical Bank Prime Rate',
                      'Market Value of Publicly Traded Shares',
                      'Exports',
                      'Imports'
                      ]
        writer = csv.DictWriter(csvfileB, fieldnames=fieldnames, lineterminator = '\n')
        writer.writeheader()
        for row in reader:
            regionName = (row['Country'])
            countryCode = (row['Code'])
            print("Getting " + regionName)
            response = requests.get('https://www.cia.gov/library/publications/the-world-factbook/geos/' + countryCode +'.html')
            soup = bs.BeautifulSoup(response.text, 'lxml')

            #Country name long and short:
            if "Country name:" not in soup.text:
                shortName = 'Not listed'
                longName = 'Not listed'
            else:
                longName = soup.body.find(text='Country name:').findNext('div')
                longName = longName.text
                shortName = soup.body.find(text='Country name:').findNext('div').findNext('div')
                shortName = shortName.text
            if "conventional long form: " in longName:
                longName = longName.split('conventional long form: ')[1]
            if "conventional short form: " in shortName:
                shortName = shortName.split('conventional short form: ')[1]
                
            #population data
            population = soup.body.find(text='Population:').findNext('div')
            population = population.text
            if "(" in population:
                popDateEst = population.split('(')[1]
                population = population.split('(')[0]
            if "total:" in population:
                population = population.split('total:')[1]
            if "United Kingdom" in population:
                population = population.split('United Kingdom')[1]
            if "million" in population:
                population = population.split(' million')[0]
                population = (float(population) * 10**6)

            #population growth rate
            if "Population growth rate:" not in soup.text:
                populationGrowth = 'Not listed'
            else:
                populationGrowth = soup.body.find(text='Population growth rate:').findNext('div')
                populationGrowth = populationGrowth.text
            if "(" in populationGrowth:
                popGrowthDateEst = populationGrowth.split('(')[1]
                populationGrowth = populationGrowth.split('(')[0]
            
            #GDP (purchasing power parity):
            if "GDP (purchasing power parity):" not in soup.text:
                GDPppp = 'Not listed'
            else:
                GDPppp = soup.body.find(text='GDP (purchasing power parity):').findNext('div')
                GDPppp = GDPppp.text
            if "(" in GDPppp:
                GDPpppDateEst = GDPppp.split('(')[1]
                GDPppp = GDPppp.split('(')[0]
            if "million" in GDPppp:
                GDPppp = GDPppp.split('million')[0]
                GDPppp = GDPppp[1:]
                GDPppp = float(GDPppp) * 10**6
            elif "billion" in GDPppp:
                GDPppp = GDPppp.split('billion')[0]
                GDPppp = GDPppp[1:]
                GDPppp = float(GDPppp) * 10**9
            elif "trillion" in GDPppp:
                GDPppp = GDPppp.split('trillion')[0]
                GDPppp = GDPppp[1:]
                GDPppp = float(GDPppp)
                GDPppp = int(GDPppp) * 10**12

            #GDP - real growth rate:
            if "GDP - real growth rate:" not in soup.text:
                RealGDPgrowth = 'Not listed'
            else:
                RealGDPgrowth = soup.body.find(text='GDP - real growth rate:').findNext('div')
                RealGDPgrowth = RealGDPgrowth.text
            if "(" in RealGDPgrowth:
                RealGDPgrowthDateEst = RealGDPgrowth.split('(')[1]
                RealGDPgrowth = RealGDPgrowth.split('(')[0]

                
            #GDP - per capita (PPP):
            if "GDP - per capita (PPP):" not in soup.text:
                GDPcapita = 'Not listed'
            else:
                GDPcapita = soup.body.find(text='GDP - per capita (PPP):').findNext('div')
                GDPcapita = GDPcapita.text
            if "(" in GDPcapita:
                GDPcapitaDateEst = GDPcapita.split('(')[1]
                GDPcapita = GDPcapita.split('(')[0]

            #Gross National Savings:
            if "Gross national saving:" not in soup.text:
                GNS = 'Not listed'
            else:
                GNS = soup.body.find(text='Gross national saving:').findNext('div')
                GNS = GNS.text
            if "(" in GNS:
                GNSDateEst = GNS.split('(')[1]
                GNS = GNS.split('(')[0]

##            #GDP by end use:
##            if "GDP - real growth rate:" not in soup.text:
##                RealGDPgrowth = 'Not listed'
##            else:
##                RealGDPgrowth = soup.body.find(text='GDP - real growth rate:').findNext('div')
##                GDPgrowth = GDPgrowth.text
##            if "(" in GDPgrowth:
##                RealGDPgrowthDateEst = GDPgrowth.split('(')[1]
##                RealGDPgrowth = GDPgrowth.split('(')[0]
##
##            #GDP by sector of origin
##            if "GDP - real growth rate:" not in soup.text:
##                RealGDPgrowth = 'Not listed'
##            else:
##                RealGDPgrowth = soup.body.find(text='GDP - real growth rate:').findNext('div')
##                GDPgrowth = GDPgrowth.text
##            if "(" in GDPgrowth:
##                RealGDPgrowthDateEst = GDPgrowth.split('(')[1]
##                RealGDPgrowth = GDPgrowth.split('(')[0]

            #Labor Force
            if "Labor force:" not in soup.text:
                LaborForce = 'Not listed'
            else:
                LaborForce = soup.body.find(text='Labor force:').findNext('div')
                LaborForce = LaborForce.text
            if "(" in LaborForce:
                LaborForceDateEst = LaborForce.split('(')[1]
                LaborForce = LaborForce.split('(')[0]

            #Unemployment Rate
            if "Unemployment rate:" not in soup.text:
                unemployment = 'Not listed'
            else:
                unemployment = soup.body.find(text='Unemployment rate:').findNext('div')
                unemployment = unemployment.text
            if "(" in unemployment:
                unemploymentDateEst = unemployment.split('(')[1]
                unemployment = unemployment.split('(')[0]
            
            #Population below poverty line:
            if "Population below poverty line:" not in soup.text:
                poverty = 'Not listed'
            else:
                poverty = soup.body.find(text='Population below poverty line:').findNext('div')
                poverty = poverty.text
            if "(" in poverty:
                povertyDateEst = poverty.split('(')[1]
                poverty = poverty.split('(')[0]

            #Inflation Rate
            if "Inflation rate (consumer prices):" not in soup.text:
                inflation = 'Not listed'
            else:
                inflation = soup.body.find(text='Inflation rate (consumer prices):').findNext('div')
                inflation = inflation.text
            if "(" in inflation:
                inflationDateEst = inflation.split('(')[1]
                inflation = inflation.split('(')[0]
            
            #Commercial Bank Prime Lending Rate
            if "Commercial bank prime lending rate:" not in soup.text:
                primeRate = 'Not listed'
            else:
                primeRate = soup.body.find(text='Commercial bank prime lending rate:').findNext('div')
                primeRate = primeRate.text
            if "(" in primeRate:
                primeRateDateEst = primeRate.split('(')[1]
                primeRate = primeRate.split('(')[0]       

            #Market Value of publicly traded shares
            if "Market value of publicly traded shares:" not in soup.text:
                publiclyTraded = 'Not listed'
            else:
                publiclyTraded = soup.body.find(text='Market value of publicly traded shares:').findNext('div')
                publiclyTraded = publiclyTraded.text
            if "(" in publiclyTraded:
                publiclyTradedDateEst = publiclyTraded.split('(')[1]
                publiclyTraded = publiclyTraded.split('(')[0]

            #Exports
            if "Exports:" not in soup.text:
                exports = 'Not listed'
            else:
                exports = soup.body.find(text='Exports:').findNext('div')
                exports = exports.text
            if "(" in exports:
                exportsDateEst = exports.split('(')[1]
                exports = exports.split('(')[0]

            #Imports
            if "Imports:" not in soup.text:
                imports = 'Not listed'
            else:
                imports = soup.body.find(text='Imports:').findNext('div')
                imports = imports.text
            if "(" in imports:
                importsDateEst = imports.split('(')[1]
                imports = imports.split('(')[0]


#other
##
##            #Median age:
##            if "Median age:" not in soup.text:
##                medianAge = 'Not listed'
##            else:
##                medianAge = soup.body.find(text='Median age:').findNext('div')
##                medianAge = medianAge.text
##            if "(" in GDPgrowth:
##                medianAgeDateEst = medianAge.split('(')[1]
##                medianAge = medianAge.split('(')[0]
##            if "total: " in medianAge:
##                medianAge = medianAge.split('total: ')[1]
##            if "years" in medianAge:
##                medianAge = medianAge.split('years')[0]
##                
##            #Capital:
##            if "Capital:" not in soup.text:
##                capital = 'Not listed'
##            else:
##                capital = soup.body.find(text='Capital:').findNext('div')
##                capital = capital.text
##            if "name: " in capital:
##                capital = capital.split('name: ')[1]
##            if "capital: " in capital:
##                capital = capital.split('capital: ')[1]

            #print to csv
            writer.writerow({'Region': regionName,
                             'Code': countryCode,
                             'Short Name': shortName,
                             'Long Name': longName,
                             'Population': population,
                             'Population Growth Rate': populationGrowth,
                             'GDP (PPP)':GDPppp ,
                             'GDP per Capita':GDPcapita,
                             'Real GDP Growth Rate':RealGDPgrowth,
                             'Gross National Savings': GNS,
                             'Labor Force': LaborForce,
                             'Unemployment Rate': unemployment,
                             'Population below poverty line': poverty,
                             'Inflation Rate': inflation,
                             'Commerical Bank Prime Rate': primeRate,
                             'Market Value of Publicly Traded Shares':publiclyTraded,
                             'Exports': exports ,
                             'Imports': imports
                             })
            
