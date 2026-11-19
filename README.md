# Smokehouse

A wood-fired food preservation bench for RimWorld 1.6 / 1.7.

Pemmican is the only travel food a low-tech colony can make, and it needs **both** meat and vegetables in the pantry at the same time. Smokehouse adds a second option: a single-ingredient preservation bench that burns wood instead of power.

A hunting colony with a freezer full of meat, a desert outpost that never sees a vegetable, a tribal start with no electricity, a gravship galley with no room for a cooler — all of them can now turn a surplus of one food type into rations that keep for a season.

Pure XML. No C#, no Harmony, no DLC required.

---

## What it adds

| | |
|---|---|
| **Research** | *Smoke preserving* — Neolithic, 600 points, requires Pemmican |
| **Building** | Smokehouse — 2x1, 55 wood + 10 steel, burns wood, no power |
| **Bills** | Smoke meat · Dry vegetables |
| **Items** | Smoked meat · Dried vegetables |
| **Mood** | +2 "ate cured provisions" for one day |

### Smoked meat
0.5 nutrition of raw meat in, 5 smoked meat out (0.6 nutrition). 45 days before rot, mass 0.025, stacks to 75.

### Dried vegetables
0.5 nutrition of raw plant food in, 6 dried vegetables out (0.6 nutrition). 60 days before rot, mass 0.02, stacks to 75.

For comparison, pemmican converts 0.5 nutrition into 0.8 nutrition but demands both food types at once. Cured provisions yield a bit less and eventually spoil; in exchange they need one ingredient, no vegetables-or-meat logistics, and nothing but firewood to run.

### The smokehouse
- 2x1 footprint, 150 HP, work speed is affected by cooking skill like any other bench
- Refuels from wood; only burns fuel while a colonist is actually working
- Pushes a little heat (3/s) — useful in a cold biome, annoying in a heatwave
- Can be uninstalled and reinstalled like any workbench, so it travels with a caravan or a gravship
- Beauty -4, because it is a smoky shed

## Installation

1. Download `rimworld-smokehouse-v1.0.0.zip` from the [Releases](../../releases) page.
2. Extract the `Smokehouse` folder into your RimWorld `Mods` folder.
   - Windows: `C:\Program Files (x86)\Steam\steamapps\common\RimWorld\Mods`
   - macOS: `~/Library/Application Support/Steam/steamapps/common/RimWorld/Mods`
   - Linux: `~/.steam/steam/steamapps/common/RimWorld/Mods`
3. Enable **Smokehouse** in the mod list and restart.

Load order: anywhere after Core. It does not patch vanilla defs, so load order barely matters.

## Compatibility

- **Versions:** 1.6 (main branch) and 1.7 (unstable branch). Everything is plain Defs XML with no version-specific code, so the same files work on both.
- **DLC:** none required. Royalty, Ideology, Biotech, Anomaly and Odyssey can all be active.
- **Mods:** no vanilla defs are patched or overwritten, so conflicts are unlikely. Modded raw meats and plant foods are picked up automatically through the `MeatRaw` / `PlantFoodRaw` categories.
- **Existing saves:** safe to add. Removing the mod mid-save will delete the smokehouse and any cured food on the map — eat it first.

## Notes

- Human meat and megaspider meat are excluded from the smoked meat bill by default, matching pemmican. Re-enable them in the bill's ingredient filter if your colony has... opinions.
- Cured provisions count as meals, so colonists still want a table. The mood thought is separate from the table thought.
- The smokehouse is flammable. Do not build it against your wooden stockpile wall. (Do build it next to one, if you like drama.)

## Credits

Art, XML and balance by rukwle9uyq. Built with the vanilla def structures as reference.

License: see [LICENSE.txt](LICENSE.txt).
