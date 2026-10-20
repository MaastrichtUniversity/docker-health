"""Unit tests for the live normalisation pipeline in ``dabs-live-demo/server.py``.

Driven by the JSON payloads in ``tests/samples/`` (materialised from
``docs/federation-samples.md``). No network access.
"""

import unittest
from unittest import mock

from support import samples
from support.server_loader import load_server

server = load_server()


class ServerCase(unittest.TestCase):
    """Pins the environment-dependent globals so tests are deterministic."""

    def setUp(self):
        self._known_nodes = server.KNOWN_NODES
        self._config = dict(server.CONFIG)
        server.KNOWN_NODES = ["zio", "mumc", "envida", "vitala"]
        server.CONFIG["eigen_node"] = "zio"

    def tearDown(self):
        server.KNOWN_NODES = self._known_nodes
        server.CONFIG.clear()
        server.CONFIG.update(self._config)


# ---------------------------------------------------------------------------
# _snake
# ---------------------------------------------------------------------------
class TestSnake(ServerCase):
    def test_lengte_datum_tijd(self):
        self.assertEqual(server._snake("LengteDatumTijd"), "lengte_datum_tijd")

    def test_contract_examples(self):
        cases = {
            "BloeddrukDatumTijd": "bloeddruk_datum_tijd",
            "GewichtWaarde": "gewicht_waarde",
            "LengteWaarde": "lengte_waarde",
            "AnatomischeLocatie": "anatomische_locatie",
            "OverlijdensIndicator": "overlijdens_indicator",
            "SystolischeBloeddruk": "systolische_bloeddruk",
            "Identificatienummer": "identificatienummer",
            "Naamgebruik": "naamgebruik",
            "EmailAdressen": "email_adressen",
            "AanduidingBijNummer": "aanduiding_bij_nummer",
            "Huisnummertoevoeging": "huisnummertoevoeging",
            "TelecomType": "telecom_type",
        }
        for live, expected in cases.items():
            with self.subTest(live=live):
                self.assertEqual(server._snake(live), expected)


# ---------------------------------------------------------------------------
# _find
# ---------------------------------------------------------------------------
class TestFind(ServerCase):
    def test_case_insensitive(self):
        self.assertEqual(server._find({"Magnitude": 5}, "magnitude"), 5)
        self.assertEqual(server._find({"units": "kg"}, "Units"), "kg")

    def test_default(self):
        self.assertIsNone(server._find({}, "Value"))
        self.assertEqual(server._find({}, "Value", default="x"), "x")

    def test_first_match_wins(self):
        self.assertEqual(server._find({"A": 1, "a": 2}, "a"), 1)


# ---------------------------------------------------------------------------
# _convert
# ---------------------------------------------------------------------------
class TestConvert(ServerCase):
    def test_measurement_unwraps(self):
        self.assertEqual(
            server._convert({"Magnitude": 139, "Units": "mm[Hg]"}),
            {"magnitude": 139, "units": "mm[Hg]"},
        )

    def test_coded_value_unwraps_to_value(self):
        self.assertEqual(
            server._convert({"Value": "Unknown", "Code": "UNK", "Terminology": "x"}),
            "Unknown",
        )

    def test_coded_value_without_terminology_unwraps(self):
        self.assertEqual(server._convert({"Value": "A", "Code": "B"}), "A")

    def test_extra_key_breaks_measurement_match(self):
        # Exact-match rule: {Magnitude, Units, Extra} is snake_cased generically.
        self.assertEqual(
            server._convert({"Magnitude": 1, "Units": "kg", "Extra": 2}),
            {"magnitude": 1, "units": "kg", "extra": 2},
        )

    def test_nested_dict_snakecases_and_unwraps(self):
        converted = server._convert({
            "AnatomischeLocatie": {"Locatie": {"Value": "Arm", "Code": "c", "Terminology": "t"}}
        })
        self.assertEqual(converted, {"anatomische_locatie": {"locatie": "Arm"}})

    def test_list_converts_elementwise(self):
        self.assertEqual(server._convert([{"Value": "A", "Code": "c"}]), ["A"])

    def test_scalar_passthrough(self):
        self.assertEqual(server._convert(5), 5)
        self.assertIsNone(server._convert(None))
        self.assertEqual(server._convert("x"), "x")

    def test_nested_list_of_measurements(self):
        self.assertEqual(
            server._convert([{"Magnitude": 1, "Units": "kg"}, {"Magnitude": 2, "Units": "kg"}]),
            [{"magnitude": 1, "units": "kg"}, {"magnitude": 2, "units": "kg"}],
        )


# ---------------------------------------------------------------------------
# normalize_live
# ---------------------------------------------------------------------------
class TestNormalizeLive(ServerCase):
    def test_flat_list_groups_by_provider(self):
        per_node = server.normalize_live(samples.load("Patient"), "Patient")
        self.assertEqual(
            sorted(per_node), ["envida_federation", "mumc_federation", "vitala_federation", "zio_federation"]
        )
        for node in samples.KNOWN_NODES:
            self.assertEqual(len(per_node[f"{node}_federation"]), 1)

    def test_flat_list_lowercases_provider_and_snakecases_record(self):
        # The grouping key is lowercased; _convert snake_cases keys but leaves values
        # untouched, so the record's provider value keeps its original case.
        per_node = server.normalize_live([{"Provider": "ZIO", "Foo": "Bar"}], "Onbekend")
        self.assertEqual(per_node, {"zio_federation": [{"provider": "ZIO", "foo": "Bar"}]})

    def test_missing_provider_becomes_onbekend(self):
        per_node = server.normalize_live([{"Foo": "Bar"}], "Onbekend")
        self.assertEqual(per_node, {"onbekend_federation": [{"foo": "Bar"}]})

    def test_old_shape_passes_through_unchanged(self):
        payload = {"successes": {"zio_federation": [{"start_time": "2024"}]}, "failures": {}}
        self.assertIs(server.normalize_live(payload, "Patient"), payload)

    def test_non_list_non_dict_passes_through(self):
        self.assertEqual(server.normalize_live("x", "Patient"), "x")


# ---------------------------------------------------------------------------
# Per-endpoint normalizers, against the samples
# ---------------------------------------------------------------------------
class TestPatientNormalizer(ServerCase):
    def setUp(self):
        super().setUp()
        self.per_node = server.normalize_live(samples.load("Patient"), "Patient")
        self.zio = self.per_node["zio_federation"][0]

    def test_overlijdens_indicator_coded_dead_is_true(self):
        self.assertIs(self.zio["overlijdens_indicator"], True)

    def test_geslacht_coded_unwraps_to_string(self):
        self.assertEqual(self.zio["geslacht"], "Unknown")

    def test_identificatienummer_stays_a_list(self):
        self.assertIsInstance(self.zio["identificatienummer"], list)
        self.assertEqual(self.zio["identificatienummer"], ["999990603"])

    def test_name_composition_fields(self):
        naam = self.zio["naamgegevens"]
        self.assertEqual(naam["voornamen"], "Johanna Petronella Maria")
        self.assertEqual(naam["voorvoegsels"], "van")
        self.assertEqual(naam["achternaam"], "Putten")
        self.assertEqual(naam["naamgebruik"], "Eigen geslachtsnaam")
        self.assertEqual(naam["titels"], "Prof")

    def test_geboortedatum_and_overlijden_date(self):
        self.assertEqual(self.zio["geboortedatum"], "1984-10-03")
        self.assertEqual(self.zio["datum_overlijden"], "2042-01-01")

    def test_all_nodes_received_the_record(self):
        for node in samples.KNOWN_NODES:
            self.assertEqual(len(self.per_node[f"{node}_federation"]), 1)


class TestBloodPressureNormalizer(ServerCase):
    def setUp(self):
        super().setUp()
        self.per_node = server.normalize_live(samples.load("Bloeddruk"), "Bloeddruk")

    def test_measurements_unfold_to_numbers_and_units(self):
        zio = self.per_node["zio_federation"][0]
        self.assertEqual(zio["systolische_bloeddruk"], 139)
        self.assertEqual(zio["systolische_bloeddruk_units"], "mm[Hg]")
        self.assertEqual(zio["diastolische_bloeddruk"], 85)
        self.assertEqual(zio["diastolische_bloeddruk_units"], "mm[Hg]")
        self.assertIsInstance(zio["systolische_bloeddruk"], int)

    def test_anatomische_locatie_object_unwraps_to_strings(self):
        zio = self.per_node["zio_federation"][0]
        self.assertEqual(
            zio["anatomische_locatie"],
            {"locatie": "Structuur van linker bovenarm", "lateraliteit": "Links"},
        )

    def test_anatomische_locatie_null_does_not_crash(self):
        envida = self.per_node["envida_federation"][0]
        self.assertIsNone(envida["anatomische_locatie"])

    def test_anatomische_locatie_string_is_defensively_wrapped(self):
        # Not present in the samples; the branch exists in the reference code.
        wrapped = server._norm_blood_pressure({"anatomische_locatie": "Bovenarm"})
        self.assertEqual(wrapped["anatomische_locatie"], {"locatie": "Bovenarm", "lateraliteit": None})

    def test_houding_coded_unwraps_to_string(self):
        zio = self.per_node["zio_federation"][0]
        self.assertEqual(zio["houding"], "Zittende positie")

    def test_houding_null_stays_null(self):
        envida = self.per_node["envida_federation"][0]
        self.assertIsNone(envida["houding"])

    def test_null_gemiddelde_bloeddruk_is_removed(self):
        zio = self.per_node["zio_federation"][0]
        self.assertNotIn("gemiddelde_bloeddruk", zio)

    def test_start_time_can_differ_from_series_date(self):
        envida = self.per_node["envida_federation"][0]
        self.assertEqual(envida["start_time"], "1983-03-16T15:34:59.427")
        self.assertEqual(envida["bloeddruk_datum_tijd"], "2021-07-04T21:03:56.351")

    def test_all_nodes_have_six_records(self):
        for node in samples.KNOWN_NODES:
            self.assertEqual(len(self.per_node[f"{node}_federation"]), 6)


class TestWeightNormalizer(ServerCase):
    def setUp(self):
        super().setUp()
        self.per_node = server.normalize_live(samples.load("Lichaamsgewicht"), "Lichaamsgewicht")

    def test_gewichtwaarde_unfolds(self):
        zio = self.per_node["zio_federation"][0]
        self.assertEqual(zio["gewichtwaarde_magnitude"], 85)
        self.assertEqual(zio["gewichtwaarde_units"], "kg")
        self.assertNotIn("gewicht_waarde", zio)

    def test_kleding_coded_unwraps_to_string(self):
        mumc = self.per_node["mumc_federation"][0]
        self.assertEqual(mumc["kleding"], "Minimale kleding")

    def test_kleding_null_stays_null(self):
        zio = self.per_node["zio_federation"][0]
        self.assertIsNone(zio["kleding"])

    def test_all_nodes_have_six_records(self):
        for node in samples.KNOWN_NODES:
            self.assertEqual(len(self.per_node[f"{node}_federation"]), 6)


class TestLengthNormalizer(ServerCase):
    def setUp(self):
        super().setUp()
        self.per_node = server.normalize_live(samples.load("LichaamsLengte"), "LichaamsLengte")

    def test_lengtewaarde_unfolds(self):
        zio = self.per_node["zio_federation"][0]
        self.assertEqual(zio["lengtewaarde_magnitude"], 184)
        self.assertEqual(zio["lengtewaarde_units"], "cm")

    def test_positie_coded_unwraps_to_string(self):
        zio = self.per_node["zio_federation"][0]
        self.assertEqual(zio["positie"], "Liggende positie")
        mumc = self.per_node["mumc_federation"][0]
        self.assertEqual(mumc["positie"], "Other")

    def test_start_time_and_series_date_differ(self):
        zio = self.per_node["zio_federation"][0]
        self.assertEqual(zio["start_time"], "2001-03-19T11:43:13.174")
        self.assertEqual(zio["lengte_datum_tijd"], "2001-03-19T10:43:13.174")


# ---------------------------------------------------------------------------
# split_payload / node_label / flatten
# ---------------------------------------------------------------------------
class TestSplitPayload(ServerCase):
    def test_envelope(self):
        successes = {"zio_federation": [{"x": 1}]}
        failures = {"mumc_federation": {"error": "boom"}}
        got_successes, got_failures = server.split_payload(
            {"successes": successes, "failures": failures}
        )
        self.assertIs(got_successes, successes)
        self.assertIs(got_failures, failures)

    def test_plain_dict_is_treated_as_successes(self):
        payload = {"zio_federation": [{"x": 1}]}
        got_successes, got_failures = server.split_payload(payload)
        self.assertIs(got_successes, payload)
        self.assertEqual(got_failures, {})

    def test_empty_envelope_defaults(self):
        got_successes, got_failures = server.split_payload({})
        self.assertEqual(got_successes, {})
        self.assertEqual(got_failures, {})


class TestNodeLabel(ServerCase):
    def test_strips_federation_suffix(self):
        self.assertEqual(server.node_label("zio_federation"), "zio")
        self.assertEqual(server.node_label("federatie_federation"), "federatie")

    def test_keeps_name_without_suffix(self):
        self.assertEqual(server.node_label("onbekend"), "onbekend")


class TestFlatten(ServerCase):
    def test_tags_source_and_sorts_by_date(self):
        per_node = {
            "zio_federation": [{"d": "2020-01-01"}, {"d": "2018-01-01"}],
            "envida_federation": [{"d": "2019-01-01"}],
        }
        rows = server.flatten(per_node, "d")
        self.assertEqual(
            [(r["d"], r["_source"]) for r in rows],
            [("2018-01-01", "zio"), ("2019-01-01", "envida"), ("2020-01-01", "zio")],
        )

    def test_missing_date_sorts_first(self):
        per_node = {"zio_federation": [{"d": "2020-01-01"}, {"x": 1}]}
        rows = server.flatten(per_node, "d")
        self.assertEqual(rows[0].get("d"), None)

    def test_does_not_mutate_input_records(self):
        original = {"d": "2020-01-01"}
        per_node = {"zio_federation": [original]}
        server.flatten(per_node, "d")
        self.assertNotIn("_source", original)

    def test_length_series_uses_lengte_datum_tijd_not_start_time(self):
        # Two records whose start_time and series date sort in opposite orders.
        per_node = {
            "a_federation": [{"start_time": "2002-01-01", "lengte_datum_tijd": "2001-01-01"}],
            "b_federation": [{"start_time": "2001-01-01", "lengte_datum_tijd": "2002-01-01"}],
        }
        self.assertEqual([r["_source"] for r in server.flatten(per_node, "lengte_datum_tijd")], ["a", "b"])
        self.assertEqual([r["_source"] for r in server.flatten(per_node, "start_time")], ["b", "a"])

    def test_sample_length_series_is_sorted_by_lengte_datum_tijd(self):
        per_node = server.normalize_live(samples.load("LichaamsLengte"), "LichaamsLengte")
        rows = server.flatten(per_node, "lengte_datum_tijd")
        dates = [r["lengte_datum_tijd"] for r in rows]
        self.assertEqual(dates, sorted(dates))
        # The zio row proves the two date fields differ.
        zio = next(r for r in rows if r["_source"] == "zio")
        self.assertNotEqual(zio["start_time"], zio["lengte_datum_tijd"])


# ---------------------------------------------------------------------------
# build_response: node statuses, KNOWN_NODES fill-in, ordering, meta
# ---------------------------------------------------------------------------
class TestBuildResponse(ServerCase):
    def build(self, endpoint_payloads, btg=False):
        def fake_get_payload(endpoint, bsn, requester, btg_flag):
            return endpoint_payloads.get(endpoint, {})

        with mock.patch.object(server, "get_payload", side_effect=fake_get_payload):
            return server.build_response("999990603", "Rolf", btg)

    @staticmethod
    def nodes_by_name(result):
        return {node["name"]: node for node in result["nodes"]}

    def test_ok_when_node_has_records(self):
        result = self.build({"Patient": {"zio_federation": [{"start_time": "2024-01-01"}]}})
        nodes = self.nodes_by_name(result)
        self.assertEqual(nodes["zio"]["status"], "ok")
        self.assertEqual(nodes["zio"]["records"], 1)
        self.assertIsNone(nodes["zio"]["message"])

    def test_consent_blocked_when_other_node_has_data_and_btg_off(self):
        result = self.build({"Patient": {"zio_federation": [{"start_time": "2024-01-01"}]}})
        nodes = self.nodes_by_name(result)
        self.assertEqual(nodes["envida"]["status"], "consent_blocked")
        self.assertEqual(nodes["envida"]["records"], 0)

    def test_geen_data_when_btg_on_and_node_has_nothing(self):
        result = self.build(
            {"Patient": {"zio_federation": [{"start_time": "2024-01-01"}]}}, btg=True
        )
        nodes = self.nodes_by_name(result)
        self.assertEqual(nodes["envida"]["status"], "geen_data")

    def test_geen_data_when_nobody_has_data(self):
        result = self.build({})
        nodes = self.nodes_by_name(result)
        self.assertTrue(all(n["status"] == "geen_data" for n in nodes.values()))

    def test_offline_from_failure_entry(self):
        result = self.build({
            "Patient": {
                "successes": {},
                "failures": {"zio_federation": {"error": "URLError", "message": "boom"}},
            }
        })
        nodes = self.nodes_by_name(result)
        self.assertEqual(nodes["zio"]["status"], "offline")
        self.assertEqual(nodes["zio"]["records"], 0)
        self.assertEqual(nodes["zio"]["message"], "boom")

    def test_known_nodes_fill_in_when_a_node_vanishes(self):
        result = self.build({"Patient": {"zio_federation": [{"start_time": "2024-01-01"}]}})
        names = {node["name"] for node in result["nodes"]}
        self.assertEqual(names, {"zio", "mumc", "envida", "vitala"})

    def test_own_node_is_first(self):
        result = self.build({})
        self.assertEqual(result["nodes"][0]["name"], "zio")
        self.assertIs(result["nodes"][0]["own"], True)
        self.assertIs(result["nodes"][1]["own"], False)

    def test_node_order_own_first_then_alphabetical(self):
        result = self.build({})
        self.assertEqual([n["name"] for n in result["nodes"]], ["zio", "envida", "mumc", "vitala"])

    def test_meta_live_only(self):
        result = self.build({})
        meta = result["meta"]
        self.assertEqual(meta["mode"], "nodes")
        self.assertIsNone(meta["dataset"])
        self.assertIsNone(meta["btg_extra_records"])
        self.assertEqual(meta["sources"], ["live"])
        self.assertIs(meta["btg"], False)
        self.assertEqual(meta["requester"], "Rolf")
        self.assertEqual(meta["eigen_node"], "zio")

    def test_bsn_is_echoed(self):
        result = self.build({})
        self.assertEqual(result["bsn"], "999990603")

    def test_series_keys_are_present(self):
        result = self.build({})
        for key in ("patient", "bloeddruk", "gewicht", "lengte"):
            self.assertIn(key, result)
            self.assertIsInstance(result[key], list)


if __name__ == "__main__":
    unittest.main()
