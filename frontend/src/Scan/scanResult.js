const BIN_MAP = {
    plastic:   { bin: 'BAC JAUNE', binColor: 'bg-yellow-400 text-yellow-900 border-yellow-500' },
    glass:     { bin: 'BAC VERT', binColor: 'bg-green-500 text-white border-green-600' },
    paper:     { bin: 'BAC BLEU', binColor: 'bg-blue-500 text-white border-blue-600' },
    cardboard: { bin: 'BAC BLEU', binColor: 'bg-blue-500 text-white border-blue-600' },
    metal:     { bin: 'BAC JAUNE', binColor: 'bg-yellow-400 text-yellow-900 border-yellow-500' },
    trash:     { bin: 'ORDURES MÉNAGÈRES', binColor: 'bg-gray-500 text-white border-gray-600' },
};

export function mapApiToUI(data) {
    const label = data.waste_class || data.label || data.class_name || 'Objet inconnu';
    const confidence = Math.round((data.confidence ?? 0) * 100);
    const category = Object.keys(BIN_MAP).find(key =>
        label.toLowerCase().includes(key)
    );
    const { bin, binColor } = BIN_MAP[category] ?? {
        bin: 'ORDURES MÉNAGÈRES',
        binColor: 'bg-gray-500 text-white border-gray-600',
    };

    return {
        label,
        confidence,
        instruction: data.sorting_instruction || data.message,
        bin,
        binColor,
        isUncertain: data.is_uncertain ?? confidence < 60,
    };
}
