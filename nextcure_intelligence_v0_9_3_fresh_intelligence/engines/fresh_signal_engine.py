from dataclasses import dataclass

@dataclass(frozen=True)
class FreshSignal:
    category:str
    signal:str
    relevance:str
    implication:str
    action:str


def build_fresh_signals():
    return [
        FreshSignal(
            category="ADC Patent Activity",
            signal="Increased industry focus on next-generation linker stability and payload tolerability in ovarian-focused ADC programs.",
            relevance="High",
            implication="Suggests the competitive landscape may increasingly reward differentiated safety/tolerability rather than simply target selection.",
            action="Track whether NXTC positioning can emphasize differentiation beyond target overlap."
        ),
        FreshSignal(
            category="Grant / Funding Drift",
            signal="Academic and translational funding continues clustering around precision oncology and biomarker-guided patient selection.",
            relevance="Medium",
            implication="Market may increasingly value companies with clearer patient stratification narratives ahead of broader oncology peers.",
            action="Monitor peer communication around biomarker strategy and enrollment quality."
        ),
        FreshSignal(
            category="Competitive Read-through",
            signal="Peer ADC commentary continues emphasizing toxicity mitigation and dosing flexibility as competitive advantages.",
            relevance="High",
            implication="Competitive edge may increasingly come from clinical usability and safety profile perception, not only efficacy signals.",
            action="Watch whether investor discussions begin rewarding durability and tolerability narratives."
        )
    ]
