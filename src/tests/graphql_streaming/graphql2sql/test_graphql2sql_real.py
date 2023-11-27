from unittest import TestCase

from gobapi.graphql_streaming.graphql2sql import graphql2sql


class TestGraphQL2SQLReal(TestCase):

    def test_full_query(self):
        """Test full query with all kinds of constructs embedded."""
        graphql = """
{
  meetboutenMeetbouten (publiceerbaar: true, active: false, sort: [identificatie_asc, status_desc]) {
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
              datum @formatdate(format: "%Y-%m-%d")
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
        expected_sql = """\
SELECT
mbt_0._gobid,
mbt_0.identificatie,
mbt_0.locatie,
mbt_0.status,
ST_AsText(mbt_0.geometrie) geometrie,
mbt_0.nabij_nummeraanduiding,
'meetbouten' AS _catalog,
'meetbouten' AS _collection,
json_build_object('_gobid', mtg_0._gobid,'identificatie', mtg_0.identificatie,'datum', mtg_0.datum, '_catalog', 'meetbouten', '_collection', 'metingen') _heeft_eerste_meting,
json_build_object('_gobid', mtg_1._gobid,'identificatie', mtg_1.identificatie,'hoogte_tov_nap', mtg_1.hoogte_tov_nap,'zakkingssnelheid', mtg_1.zakkingssnelheid,'zakking_cumulatief', mtg_1.zakking_cumulatief, '_catalog', 'meetbouten', '_collection', 'metingen') _heeft_laatste_meting,
json_build_object('_gobid', bbk_0._gobid,'identificatie', bbk_0.identificatie,'code', bbk_0.code, '_catalog', 'gebieden', '_collection', 'bouwblokken') _ligt_in_bouwblok,
json_build_object('_gobid', brt_0._gobid,'identificatie', brt_0.identificatie,'code', brt_0.code,'naam', brt_0.naam, '_catalog', 'gebieden', '_collection', 'buurten') _ligt_in_buurt,
json_build_object('_gobid', sdl_0._gobid,'identificatie', sdl_0.identificatie,'code', sdl_0.code,'naam', sdl_0.naam, '_catalog', 'gebieden', '_collection', 'stadsdelen') _ligt_in_stadsdeel
FROM (
    SELECT *
    FROM legacy.meetbouten_meetbouten
    WHERE publiceerbaar = True AND _date_deleted IS NULL
    ORDER BY identificatie ASC,status DESC
    
) mbt_0

LEFT JOIN legacy.mv_mbn_mtg_mbn_mbt_hoort_bij_meetbout rel_0 ON rel_0._gobid IN (
    SELECT _gobid
    FROM legacy.mv_mbn_mtg_mbn_mbt_hoort_bij_meetbout rel
    WHERE rel.dst_id = mbt_0._id
    LIMIT 1
)

LEFT JOIN legacy.meetbouten_metingen mtg_0 ON rel_0.src_id = mtg_0._id

LEFT JOIN legacy.mv_mbn_mtg_mbn_mbt_hoort_bij_meetbout rel_1 ON rel_1._gobid IN (
    SELECT _gobid
    FROM legacy.mv_mbn_mtg_mbn_mbt_hoort_bij_meetbout rel
    WHERE rel.dst_id = mbt_0._id
    LIMIT 1
)

LEFT JOIN legacy.meetbouten_metingen mtg_1 ON rel_1.src_id = mtg_1._id
LEFT JOIN legacy.mv_mbn_mbt_gbd_bbk_ligt_in_bouwblok rel_2 ON rel_2.src_id = mbt_0._id
LEFT JOIN legacy.gebieden_bouwblokken bbk_0 ON rel_2.dst_id = bbk_0._id AND rel_2.dst_volgnummer = bbk_0.volgnummer
LEFT JOIN legacy.mv_mbn_mbt_gbd_brt_ligt_in_buurt rel_3 ON rel_3.src_id = mbt_0._id
LEFT JOIN legacy.gebieden_buurten brt_0 ON rel_3.dst_id = brt_0._id AND rel_3.dst_volgnummer = brt_0.volgnummer
LEFT JOIN legacy.mv_mbn_mbt_gbd_sdl_ligt_in_stadsdeel rel_4 ON rel_4.src_id = mbt_0._id
LEFT JOIN legacy.gebieden_stadsdelen sdl_0 ON rel_4.dst_id = sdl_0._id AND rel_4.dst_volgnummer = sdl_0.volgnummer
ORDER BY mbt_0._gobid"""

        g2s = graphql2sql.GraphQL2SQL(graphql)
        sql = g2s.sql()
        self.assertEquals(sql.strip(), expected_sql.strip())
