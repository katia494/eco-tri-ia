import test from 'node:test';
import assert from 'node:assert/strict';

import { mapApiToUI } from './scanResult.js';


test('transforme une prédiction plastique fiable en bac jaune', () => {
    const result = mapApiToUI({
        waste_class: 'plastic',
        confidence: 0.78,
        sorting_instruction: 'Videz puis triez.',
        is_uncertain: false,
    });

    assert.equal(result.label, 'plastic');
    assert.equal(result.confidence, 78);
    assert.equal(result.bin, 'BAC JAUNE');
    assert.equal(result.isUncertain, false);
});

test('signale une confiance inférieure à 60 pour une ancienne réponse API', () => {
    const result = mapApiToUI({
        waste_class: 'paper',
        confidence: 0.52,
        message: 'Résultat à vérifier.',
    });

    assert.equal(result.confidence, 52);
    assert.equal(result.isUncertain, true);
});

test('respecte explicitement is_uncertain renvoyé par le backend', () => {
    const result = mapApiToUI({
        waste_class: 'metal',
        confidence: 0.75,
        is_uncertain: true,
    });

    assert.equal(result.isUncertain, true);
});
