from unittest import TestCase

from gobapi.graphql_streaming.graphql2sql import graphql2sql


class TestGraphQL2SQLReal(TestCase):

    def test_gebieden_bouwblokken_csv_actueel_en_historie(self):
        graphql = """
{
  meetboutenMeetbouten (publiceerbaar: true, active: false) {
    edges {
      node {
        identificatie
        locatie
        status
        geometrie
        heeftEersteMeting: invHoortBijMeetboutMeetboutenMetingen (first: 1, active: false, sort:datum_asc) {
          edges {
            node {
              identificatie
              datum
            }
          }
        }
        heeftLaatsteMeting: invHoortBijMeetboutMeetboutenMetingen (first: 1, active: false, sort: datum_desc) {
          edges {
            node {
              identificatie
              hoogteTovNap
              zakkingssnelheid
              zakkingCumulatief
            }
          }
        }
        ligtInBouwblok (active: false) {
          edges {
            node {
              identificatie
              code
            }
          }
        }
        ligtInBuurt (active: false) {
          edges {
            node {
              identificatie
              code
              naam
            }
          }
        }
        ligtInStadsdeel (active: false) {
          edges {
            node {
              identificatie
              code
              naam
            }
          }
        }
        nabijNummeraanduiding
      }
    }
  }
}
"""
        g2s = graphql2sql.GraphQL2SQL(graphql)
        sql = g2s.sql()
        print(sql)