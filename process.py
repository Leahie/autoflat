from psd_tools import PSDImage
from psd_tools.api.layers import Layer, Group, PixelLayer
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

psd = PSDImage.open("e1.psd")
print(psd)

# Get all visible layers using recursion 
def get_visible_layers(group, newpsd):
    layers = []
    for layer in group:
        if layer.is_group():
            layers.extend(get_visible_layers(layer, newpsd))
        elif layer.is_visible():
            img = layer.topil()  # Extract pixel data
            new_layer = PixelLayer(
                psd=newpsd, record=layer._record, channels=layer._channels, parent=None
            )
            layers.append(new_layer)
    return layers

# Creates psd from the layers 
def create_psd_from_layers(group, layers):
    new_group = Group.new(name="visible layers")
    for i, elm in enumerate(reversed(layers)):
        new_group.insert(index=i, layer=elm)
    new_psd = PSDImage.new(mode='RGB',size=(group.bbox[2], group.bbox[3]),color=255 )
    new_psd._layers.insert(0, new_group)  # Add group to root level
    return new_psd

new_psd = PSDImage.new(mode='RGB',size=(psd.bbox[2], psd.bbox[3]),color=255 )
layers = get_visible_layers(psd,new_psd)
new_psd = create_psd_from_layers(psd, layers)

print(new_psd.numpy())
for layer in new_psd[0]:
    print(layer)
    plt.imshow(layer.numpy())
    plt.show()


new_psd.save('output.psd') # Saving currently doesn't work 
composite = new_psd.composite() 
composite.save("output.png", format='PNG')


